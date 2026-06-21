# Portability And Determinism Repair

The seam writes a runtime dependency manifest and an isolated CLI portability result. The portability proof copies declared dependencies into two temporary roots, runs the public CLI from unrelated working directories, compares generated output hashes, and scans for absolute path leaks.
