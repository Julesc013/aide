/* Disposable H1 denial probe: synthetic paths only, no cleanup or credentials. */
#define WIN32_LEAN_AND_MEAN
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>

static DWORD observe_missing_capability(const wchar_t *literal, int *kind) {
    typedef DWORD (WINAPI *DIAGNOSE)(LPCWSTR, int *);
    union { FARPROC address; DIAGNOSE diagnose; } function;
    HMODULE module = LoadLibraryExW(L"FirewallAPI.dll", NULL, LOAD_LIBRARY_SEARCH_SYSTEM32);
    DWORD error;
    *kind = -1;
    if (!module) return GetLastError();
    function.address = GetProcAddress(module, "NetworkIsolationDiagnoseConnectFailureAndGetInfo");
    error = function.address ? function.diagnose(literal, kind) : GetLastError();
    FreeLibrary(module);
    return error;
}

static DWORD open_error(const wchar_t *path, DWORD access) {
    HANDLE value = CreateFileW(path, access, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                               NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (value != INVALID_HANDLE_VALUE) {
        CloseHandle(value);
        return ERROR_SUCCESS;
    }
    return GetLastError();
}

static int observe_network_error(const wchar_t *literal, unsigned short port) {
    WSADATA data;
    SOCKET connection;
    struct sockaddr_in address;
    u_long nonblocking = 1;
    int error = WSAStartup(MAKEWORD(2, 2), &data);
    ULONGLONG deadline = GetTickCount64() + 5000;
    if (error != 0) return error;
    connection = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (connection == INVALID_SOCKET) {
        error = WSAGetLastError();
    } else {
        ZeroMemory(&address, sizeof(address));
        address.sin_family = AF_INET;
        address.sin_port = htons(port);
        if (InetPtonW(AF_INET, literal, &address.sin_addr) != 1) {
            closesocket(connection); WSACleanup(); return WSAEINVAL;
        }
        if (ioctlsocket(connection, FIONBIO, &nonblocking) != 0) {
            error = WSAGetLastError();
        } else if (connect(connection, (const struct sockaddr *)&address, sizeof(address)) == SOCKET_ERROR) {
            error = WSAGetLastError();
            if (error == WSAEWOULDBLOCK) {
                /* A pending connect proves neither denial nor success. Wait
                   once for completion; never reconnect/retry after uncertainty. */
                fd_set writable, failed;
                struct timeval timeout;
                ULONGLONG now = GetTickCount64();
                ULONGLONG remaining = now < deadline ? deadline - now : 0;
                int ready;
                FD_ZERO(&writable); FD_SET(connection, &writable);
                FD_ZERO(&failed); FD_SET(connection, &failed);
                timeout.tv_sec = (long)(remaining / 1000);
                timeout.tv_usec = (long)((remaining % 1000) * 1000);
                ready = select(0, NULL, &writable, &failed, &timeout);
                if (GetTickCount64() >= deadline || ready == 0) {
                    error = WSAETIMEDOUT;
                } else if (ready == SOCKET_ERROR) {
                    error = WSAGetLastError();
                } else {
                    int length = sizeof(error);
                    if (getsockopt(connection, SOL_SOCKET, SO_ERROR, (char *)&error, &length) == SOCKET_ERROR) {
                        error = WSAGetLastError();
                    } else if (length != sizeof(error) ||
                               (error == 0 && (!FD_ISSET(connection, &writable) || FD_ISSET(connection, &failed)))) {
                        error = WSAEINVAL; /* Ambiguous completion never qualifies. */
                    }
                }
            }
        }
        closesocket(connection);
    }
    WSACleanup();
    return error;
}

static int canonical_ipv4(const wchar_t *literal, IN_ADDR *address) {
    wchar_t canonical[16];
    return wcslen(literal) <= 15 && InetPtonW(AF_INET, literal, address) == 1 &&
           InetNtopW(AF_INET, address, canonical, 16) != NULL && wcscmp(literal, canonical) == 0;
}

static int observe_local_interface(const wchar_t *literal, const wchar_t *index_text, const wchar_t *alias) {
    MIB_UNICASTIPADDRESS_ROW address = {0};
    MIB_IF_ROW2 adapter = {0};
    IN_ADDR expected;
    wchar_t *end = NULL;
    unsigned long index = wcstoul(index_text, &end, 10);
    DWORD address_error, adapter_error;
    if (!index || !end || *end || wcslen(alias) > IF_MAX_STRING_SIZE || !canonical_ipv4(literal, &expected)) return 70;
    address.Address.si_family = AF_INET;
    address.Address.Ipv4.sin_addr = expected;
    address.InterfaceIndex = index;
    address_error = GetUnicastIpAddressEntry(&address);
    adapter.InterfaceIndex = index;
    adapter_error = GetIfEntry2(&adapter);
    printf("{\"address_status\":%lu,\"adapter_status\":%lu,\"address_match\":%d,"
           "\"index_match\":%d,\"alias_match\":%d,\"preferred\":%d,\"connected\":%d,"
           "\"prefix_length\":%u,\"skip_as_source\":%u}\n",
           address_error, adapter_error,
           address_error == NO_ERROR && address.Address.si_family == AF_INET && address.Address.Ipv4.sin_addr.s_addr == expected.s_addr,
           address_error == NO_ERROR && adapter_error == NO_ERROR && address.InterfaceIndex == index && adapter.InterfaceIndex == index &&
               address.InterfaceLuid.Value == adapter.InterfaceLuid.Value,
           adapter_error == NO_ERROR && wcscmp(adapter.Alias, alias) == 0,
           address_error == NO_ERROR && address.DadState == IpDadStatePreferred,
           adapter_error == NO_ERROR && adapter.OperStatus == IfOperStatusUp && adapter.MediaConnectState == MediaConnectStateConnected,
           (unsigned int)address.OnLinkPrefixLength, (unsigned int)address.SkipAsSource);
    return address_error == NO_ERROR && adapter_error == NO_ERROR ? 0 : 75;
}

int wmain(int argc, wchar_t **argv) {
    wchar_t scratch[1024];
    IN_ADDR parsed;
    wchar_t *end = NULL;
    unsigned long parent, port;
    HANDLE file, process;
    DWORD written = 0, scratch_error, read_error, write_error, dacl_error, process_error;
    int network_error = 0, missing_capability = -1;
    DWORD diagnostic_status;
    const char sample[] = "owned-native-probe";
    /* Read-only local identity observation has no socket/listener/file effect. */
    if (argc == 5 && wcscmp(argv[1], L"--local-interface") == 0)
        return observe_local_interface(argv[2], argv[3], argv[4]);
    /* Ordinary oracle: image/literal/port. Isolated: image/scratch/canary/
       controller/literal/port. Both diagnose exactly the connected address. */
    if (argc == 3) {
        port = wcstoul(argv[2], &end, 10);
        if (!port || port > 65535 || !end || *end || !canonical_ipv4(argv[1], &parsed)) return 70;
        network_error = observe_network_error(argv[1], (unsigned short)port);
        diagnostic_status = observe_missing_capability(argv[1], &missing_capability);
        printf("{\"network_error\":%d,\"diagnostic_status\":%lu,\"missing_capability\":%d}\n",
               network_error, diagnostic_status, missing_capability);
        return network_error == 0 ? 0 : 74;
    }
    if (argc != 6 || wcslen(argv[1]) > 900 || wcslen(argv[2]) > 900 || !canonical_ipv4(argv[4], &parsed)) return 70;
    parent = wcstoul(argv[3], &end, 10);
    if (!parent || !end || *end) return 70;
    port = wcstoul(argv[5], &end, 10);
    if (!port || port > 65535 || !end || *end) return 70;
    if (swprintf_s(scratch, 1024, L"%ls\\native-created.txt", argv[1]) < 0) return 70;
    file = CreateFileW(scratch, GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
    scratch_error = file == INVALID_HANDLE_VALUE ? GetLastError() : ERROR_SUCCESS;
    if (file != INVALID_HANDLE_VALUE) {
        if (!WriteFile(file, sample, (DWORD)(sizeof(sample) - 1), &written, NULL) ||
                written != sizeof(sample) - 1 || !FlushFileBuffers(file)) {
            scratch_error = GetLastError();
            if (scratch_error == ERROR_SUCCESS) scratch_error = ERROR_WRITE_FAULT;
        }
        CloseHandle(file);
    }
    read_error = open_error(argv[2], GENERIC_READ);
    write_error = open_error(argv[2], GENERIC_WRITE);
    dacl_error = open_error(argv[2], WRITE_DAC);
    process = OpenProcess(PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_CREATE_THREAD | PROCESS_DUP_HANDLE,
                          FALSE, (DWORD)parent);
    process_error = process ? ERROR_SUCCESS : GetLastError();
    if (process) CloseHandle(process);
    network_error = observe_network_error(argv[4], (unsigned short)port);
    diagnostic_status = observe_missing_capability(argv[4], &missing_capability);
    printf("{\"scratch_error\":%lu,\"read_error\":%lu,\"write_error\":%lu,"
           "\"dacl_error\":%lu,\"controller_error\":%lu,\"network_error\":%d,"
           "\"diagnostic_status\":%lu,\"missing_capability\":%d}\n",
           scratch_error, read_error, write_error, dacl_error, process_error, network_error, diagnostic_status, missing_capability);
    return scratch_error == ERROR_SUCCESS && read_error == ERROR_ACCESS_DENIED &&
           write_error == ERROR_ACCESS_DENIED && dacl_error == ERROR_ACCESS_DENIED &&
           process_error == ERROR_ACCESS_DENIED && diagnostic_status == ERROR_SUCCESS &&
           missing_capability >= 1 && missing_capability <= 3 &&
           (network_error == WSAEACCES || network_error == WSAETIMEDOUT) ? 0 : 73;
    /* The host must additionally prove exact non-exemption and positive
       controls on the same listener; this exit code alone never qualifies. */
}
