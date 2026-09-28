"""Windows-only owned process execution. No PID-based killing or shell dispatch.

PROC_THREAD_ATTRIBUTE_JOB_LIST assigns the child to a kill-on-close Job during
CreateProcess itself. This avoids the suspended-but-not-yet-assigned orphan gap.
This is process containment, NOT a filesystem/credential security sandbox.
"""
from __future__ import annotations

from contextlib import nullcontext
import ctypes as C
from ctypes import wintypes as W
import os
from pathlib import Path
import subprocess
import threading
import time

from .state import Refused

JOB_PREFIX = "Local\\AIDEContinuous-"


if os.name == "nt":
    K = C.WinDLL("kernel32", use_last_error=True)
    SIZE = C.c_size_t

    class IO_COUNTERS(C.Structure):
        _fields_ = [(n, C.c_ulonglong) for n in
                    ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                     "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

    class BASIC_LIMIT(C.Structure):
        _fields_ = [("PerProcessUserTimeLimit", C.c_longlong), ("PerJobUserTimeLimit", C.c_longlong),
                    ("LimitFlags", W.DWORD), ("MinimumWorkingSetSize", SIZE),
                    ("MaximumWorkingSetSize", SIZE), ("ActiveProcessLimit", W.DWORD),
                    ("Affinity", SIZE), ("PriorityClass", W.DWORD), ("SchedulingClass", W.DWORD)]

    class EXTENDED_LIMIT(C.Structure):
        _fields_ = [("BasicLimitInformation", BASIC_LIMIT), ("IoInfo", IO_COUNTERS),
                    ("ProcessMemoryLimit", SIZE), ("JobMemoryLimit", SIZE),
                    ("PeakProcessMemoryUsed", SIZE), ("PeakJobMemoryUsed", SIZE)]

    class ACCOUNTING(C.Structure):
        _fields_ = [("TotalUserTime", C.c_longlong), ("TotalKernelTime", C.c_longlong),
                    ("ThisPeriodTotalUserTime", C.c_longlong), ("ThisPeriodTotalKernelTime", C.c_longlong),
                    ("TotalPageFaultCount", W.DWORD), ("TotalProcesses", W.DWORD),
                    ("ActiveProcesses", W.DWORD), ("TotalTerminatedProcesses", W.DWORD)]

    class STARTUP(C.Structure):
        _fields_ = [("cb", W.DWORD), ("lpReserved", W.LPWSTR), ("lpDesktop", W.LPWSTR),
                    ("lpTitle", W.LPWSTR), ("dwX", W.DWORD), ("dwY", W.DWORD),
                    ("dwXSize", W.DWORD), ("dwYSize", W.DWORD), ("dwXCountChars", W.DWORD),
                    ("dwYCountChars", W.DWORD), ("dwFillAttribute", W.DWORD),
                    ("dwFlags", W.DWORD), ("wShowWindow", W.WORD), ("cbReserved2", W.WORD),
                    ("lpReserved2", C.POINTER(C.c_byte)), ("hStdInput", W.HANDLE),
                    ("hStdOutput", W.HANDLE), ("hStdError", W.HANDLE)]

    class STARTUP_EX(C.Structure):
        _fields_ = [("StartupInfo", STARTUP), ("lpAttributeList", C.c_void_p)]

    class PROCESS(C.Structure):
        _fields_ = [("hProcess", W.HANDLE), ("hThread", W.HANDLE),
                    ("dwProcessId", W.DWORD), ("dwThreadId", W.DWORD)]

    def bind(name, args, result):
        f = getattr(K, name)
        f.argtypes, f.restype = args, result
        return f

    create_job = bind("CreateJobObjectW", [C.c_void_p, W.LPCWSTR], W.HANDLE)
    open_job = bind("OpenJobObjectW", [W.DWORD, W.BOOL, W.LPCWSTR], W.HANDLE)
    close = bind("CloseHandle", [W.HANDLE], W.BOOL)
    set_job = bind("SetInformationJobObject", [W.HANDLE, C.c_int, C.c_void_p, W.DWORD], W.BOOL)
    query_job = bind("QueryInformationJobObject", [W.HANDLE, C.c_int, C.c_void_p, W.DWORD, C.c_void_p], W.BOOL)
    terminate_job = bind("TerminateJobObject", [W.HANDLE, W.UINT], W.BOOL)
    init_attrs = bind("InitializeProcThreadAttributeList", [C.c_void_p, W.DWORD, W.DWORD, C.POINTER(SIZE)], W.BOOL)
    update_attr = bind("UpdateProcThreadAttribute", [C.c_void_p, W.DWORD, SIZE, C.c_void_p, SIZE, C.c_void_p, C.c_void_p], W.BOOL)
    delete_attrs = bind("DeleteProcThreadAttributeList", [C.c_void_p], None)
    create_process = bind("CreateProcessW", [W.LPCWSTR, W.LPWSTR, C.c_void_p, C.c_void_p, W.BOOL,
                                           W.DWORD, C.c_void_p, W.LPCWSTR, C.c_void_p, C.c_void_p], W.BOOL)
    resume = bind("ResumeThread", [W.HANDLE], W.DWORD)
    wait = bind("WaitForSingleObject", [W.HANDLE, W.DWORD], W.DWORD)
    exit_code = bind("GetExitCodeProcess", [W.HANDLE, C.POINTER(W.DWORD)], W.BOOL)
    process_times = bind("GetProcessTimes", [W.HANDLE, C.POINTER(W.FILETIME), C.POINTER(W.FILETIME),
                         C.POINTER(W.FILETIME), C.POINTER(W.FILETIME)], W.BOOL)
    current_process = bind("GetCurrentProcess", [], W.HANDLE)
    process_in_job = bind("IsProcessInJob", [W.HANDLE, W.HANDLE, C.POINTER(W.BOOL)], W.BOOL)

    def check(ok):
        if not ok:
            raise C.WinError(C.get_last_error())

    def active(job):
        info = ACCOUNTING()
        check(query_job(job, 1, C.byref(info), C.sizeof(info), None))
        return info.ActiveProcesses


def sanitized_environment():
    # Do not forward arbitrary provider, GitHub, cloud credentials or Python hooks.
    allowed = ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "PATHEXT", "TEMP", "TMP",
               "USERPROFILE", "LOCALAPPDATA", "APPDATA", "PROGRAMFILES", "PROGRAMFILES(X86)")
    env = {k: v for k, v in os.environ.items() if k.upper() in allowed}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", GIT_TERMINAL_PROMPT="0",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return env


class WindowsJobHost:
    def _require(self, job_id):
        if os.name != "nt":
            raise Refused("this pilot host is qualified for Windows only")
        if len(job_id) != 32 or any(c not in "0123456789abcdef" for c in job_id):
            raise Refused("invalid job identity")

    def reconcile(self, job_id):
        """Terminate only the exact named owned Job; never fall back to a PID."""
        self._require(job_id)
        job = open_job(0x0004 | 0x0008, False, JOB_PREFIX + job_id)  # QUERY | TERMINATE
        if not job:
            if C.get_last_error() == 2:
                # All child creation is atomic with JOB_LIST; no named Job remains.
                return {"quiescent": True, "observation": "owned_job_absent"}
            raise C.WinError(C.get_last_error())
        try:
            check(terminate_job(job, 125))
            deadline = time.monotonic() + 10
            while active(job) and time.monotonic() < deadline:
                time.sleep(.02)
            if active(job):
                raise Refused("owned processes still active")
            return {"quiescent": True, "observation": "owned_job_terminated"}
        finally:
            close(job)

    def contains_current_process(self, job_id):
        self._require(job_id)
        job = open_job(0x0004, False, JOB_PREFIX + job_id)
        if not job:
            if C.get_last_error() == 2: return False
            raise C.WinError(C.get_last_error())
        try:
            contained = W.BOOL()
            check(process_in_job(current_process(), job, C.byref(contained)))
            return bool(contained.value)
        finally:
            close(job)

    def run(self, argv, *, cwd, input_bytes, output_dir, job_id, timeout,
            output_limit, memory_limit, process_limit, cancelled=lambda: False,
            checkpoint=lambda stage: None, security=None, environment=None,
            observed=lambda sample: None):
        self._require(job_id)
        import msvcrt

        if not argv or not Path(argv[0]).is_absolute() or not Path(argv[0]).is_file():
            raise Refused("executable must be a registered absolute file")
        if security is not None:
            security.assert_launch(argv, cwd)
            if environment is not None:
                raise Refused("environment override forbidden for protected execution")
        if environment is not None and (not isinstance(environment, dict) or
                any(not isinstance(k, str) or not k or '=' in k or '\0' in k or
                    not isinstance(v, str) or '\0' in v for k, v in environment.items())):
            raise Refused("invalid process environment")
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=False)
        stdin_path = output_dir / "stdin"
        stdin_path.write_bytes(input_bytes)
        C.set_last_error(0)
        job = create_job(None, JOB_PREFIX + job_id)
        if not job:
            raise C.WinError(C.get_last_error())
        if C.get_last_error() == 183:
            close(job)
            raise Refused("job identity already exists")
        proc = PROCESS()
        attrs = None
        fds, readers = [], []
        stop = threading.Event()
        lock = threading.Lock()
        used = 0
        reader_errors = []

        def drain(fd, path):
            nonlocal used
            try:
                with os.fdopen(fd, "rb", buffering=0) as src, open(path, "xb") as dst:
                    while chunk := src.read(8192):
                        with lock:
                            take = min(len(chunk), max(0, output_limit - used))
                            if take:
                                dst.write(chunk[:take])
                                used += take
                            if take != len(chunk):
                                stop.set()
            except BaseException as exc:
                reader_errors.append(type(exc).__name__)
                stop.set()

        try:
            limits = EXTENDED_LIMIT()
            limits.BasicLimitInformation.LimitFlags = 0x2000 | 0x8 | 0x200  # KILL_ON_JOB_CLOSE, process count, job memory
            limits.BasicLimitInformation.ActiveProcessLimit = process_limit
            limits.JobMemoryLimit = memory_limit
            check(set_job(job, 9, C.byref(limits), C.sizeof(limits)))
            with open(stdin_path, "rb") as src, (security.attributes() if security is not None else nullcontext(())) as security_attrs:
                si = STARTUP_EX()
                si.StartupInfo.cb = C.sizeof(si)
                si.StartupInfo.dwFlags = 0x100
                child_handles = [msvcrt.get_osfhandle(src.fileno())]
                for label in ("stdout", "stderr"):
                    rd, wr = os.pipe()
                    fds.append(wr)
                    child_handles.append(msvcrt.get_osfhandle(wr))
                    thread = threading.Thread(target=drain, args=(rd, output_dir / label), daemon=True)
                    thread.start()
                    readers.append(thread)
                for handle in child_handles:
                    os.set_handle_inheritable(handle, True)
                si.StartupInfo.hStdInput, si.StartupInfo.hStdOutput, si.StartupInfo.hStdError = child_handles
                if len(security_attrs) != (1 if security is not None else 0):
                    raise Refused("one exact AppContainer security attribute required")
                attribute_count = 2 + len(security_attrs)
                size = SIZE()
                init_attrs(None, attribute_count, 0, C.byref(size))
                attrs = C.create_string_buffer(size.value)
                check(init_attrs(attrs, attribute_count, 0, C.byref(size)))
                si.lpAttributeList = C.cast(attrs, C.c_void_p)
                handle_list = (W.HANDLE * 3)(*child_handles)
                job_list = (W.HANDLE * 1)(job)
                check(update_attr(attrs, 0, 0x20002, handle_list, C.sizeof(handle_list), None, None))
                check(update_attr(attrs, 0, 0x2000D, job_list, C.sizeof(job_list), None, None))
                for attribute, value, length in security_attrs:
                    if attribute != 0x20009:
                        raise Refused("unexpected security launch attribute")
                    check(update_attr(attrs, 0, attribute, value, length, None, None))
                env = (security.environment() if security is not None else
                       environment if environment is not None else sanitized_environment())
                environment = C.create_unicode_buffer("\0".join(k + "=" + v for k, v in sorted(env.items(), key=lambda x: x[0].upper())) + "\0\0")
                command = C.create_unicode_buffer(subprocess.list2cmdline([str(v) for v in argv]))
                if security is not None:
                    security.assert_launch(argv, cwd)
                checkpoint("before_create")
                if security is not None:
                    security.assert_launch(argv, cwd)
                check(create_process(str(argv[0]), command, None, None, True,
                                     0x4 | 0x80000 | 0x400 | 0x8000000,
                                     environment, str(cwd), C.byref(si), C.byref(proc)))
                times = [W.FILETIME() for _ in range(4)]
                check(process_times(proc.hProcess, *[C.byref(t) for t in times]))
                created = (times[0].dwHighDateTime << 32) | times[0].dwLowDateTime
                observed({"pid": proc.dwProcessId, "creation_filetime": created,
                          "job_id": job_id, "stage": "created_suspended"})
                checkpoint("created_suspended")
                if security is not None:
                    security.verify_child(proc.hProcess, job)
                    checkpoint("security_verified")
                    security.assert_launch(argv, cwd)
                # No child instruction has executed outside the owned Job.
                check(resume(proc.hThread) != 0xFFFFFFFF)
                checkpoint("resumed")
                for handle in child_handles:
                    os.set_handle_inheritable(handle, False)
                for fd in fds:
                    os.close(fd)
                fds.clear()
                deadline = time.monotonic() + timeout
                reason = "exited"
                next_observation = 0.0
                while wait(proc.hProcess, 25) == 258:
                    if time.monotonic() >= next_observation:
                        usage = EXTENDED_LIMIT()
                        check(query_job(job, 9, C.byref(usage), C.sizeof(usage), None))
                        observed({"pid": proc.dwProcessId, "creation_filetime": created,
                                  "job_id": job_id, "stage": "running",
                                  "peak_memory_bytes": usage.PeakJobMemoryUsed})
                        next_observation = time.monotonic() + 1.0
                    if cancelled():
                        reason = "cancelled"
                    elif stop.is_set():
                        reason = "output_limit_or_io_error"
                    elif time.monotonic() >= deadline:
                        reason = "timeout"
                    else:
                        continue
                    check(terminate_job(job, 124))
                    break
                # Even a successful parent may have left descendants. Terminate and account for them.
                check(terminate_job(job, 125))
                quiescence = time.monotonic() + 10
                while active(job) and time.monotonic() < quiescence:
                    time.sleep(.02)
                if active(job):
                    raise Refused("owned descendants did not quiesce")
                final_usage = EXTENDED_LIMIT()
                check(query_job(job, 9, C.byref(final_usage), C.sizeof(final_usage), None))
                observed({"pid": proc.dwProcessId, "creation_filetime": created,
                          "job_id": job_id, "stage": "quiescent",
                          "peak_memory_bytes": final_usage.PeakJobMemoryUsed})
                code = W.DWORD()
                check(exit_code(proc.hProcess, C.byref(code)))
                for thread in readers:
                    thread.join(5)
                if any(thread.is_alive() for thread in readers):
                    raise Refused("output drain did not finish")
                if stop.is_set() and reason == "exited":
                    reason = "output_limit_or_io_error"
                return {"exit_code": code.value, "reason": reason, "quiescent": True,
                        "bytes": used, "io_errors": reader_errors, "job_id": job_id,
                        "pid": proc.dwProcessId, "creation_filetime": created}
        finally:
            # KILL_ON_JOB_CLOSE is also effective if this interpreter dies abruptly.
            if proc.hThread:
                close(proc.hThread)
            if proc.hProcess:
                close(proc.hProcess)
            close(job)
            if attrs is not None:
                delete_attrs(attrs)
            for fd in fds:
                os.close(fd)
            for thread in readers:
                thread.join(5)
