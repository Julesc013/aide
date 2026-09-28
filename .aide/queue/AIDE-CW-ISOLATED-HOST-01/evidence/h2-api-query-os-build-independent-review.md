# Exact OS-build source review custody

Independent reviewer `/root/native_os_build_review` returned **ACCEPT for
source integration only** for commit
`d995783a2028f5c9d6c8e569a083fe190a10b4ea`, tree
`6d8e67ab999fd96414ac5ea7463ca47765fdc747`, parent/base dev
`2aaee82e96d275d83501785a073f6ba73c7b6594`.

External original: approved D control root
`reviews/native-os-build-d995783a-review.md`, SHA-256
`842f3378979248364c1fb70765531ab97254bbab16e8e5876c6842dbd4d5d2c4`.
The reviewer verified the documented `RtlGetVersion` signature and x64
structure, strict status/version refusal, nine allowed paths, exact new
manifest (SHA-256 `800fded315f7c78619df1724a37baf62c9042e31ae95207b86584f1b80b0e35e`),
unchanged prior manifest, and a clean diff. They did not rerun tests.

Postcommit managed suite `0d03c1d92a3e4ab0979d1c81f5324728` passed 53
cases, exit 0, peak memory 30,748,672 bytes, scratch retired, reservation
released. Read-only OS-version job `28ed5b32eb6440e3bcee777e5ea0ad3a`
observed running/Python OS/kernel32 builds 19045/19045/19041.

The verdict does not admit the native 180-name API-set query. Source
integration is deferred while the Lite release effect is frozen; the task
branch preserves the accepted candidate. Before dev integration, check the
exact release dependency delta and the then-current dev head.
