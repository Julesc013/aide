# Portability Isolation

Portable roots are copied from the serialized runtime dependency manifest after digest/path validation. Isolated subprocesses run with sanitized Python environment, isolated mode, unrelated working directories, import closure checks, output-set checks, and path leak scans.
