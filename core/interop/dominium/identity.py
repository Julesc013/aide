"""Repository identity parsing for the Dominium read-only seam."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


DEFAULT_DOMINIUM_IDENTITY = "github.com/julesc013/dominium"


class RepositoryIdentityError(ValueError):
    """Raised when a repository remote cannot prove the expected identity."""


@dataclass(frozen=True)
class RepositoryIdentity:
    host: str
    owner: str
    repository: str
    transport: str
    canonical_identity: str

    def as_dict(self) -> dict[str, str]:
        return {
            "host": self.host,
            "owner": self.owner,
            "repository": self.repository,
            "transport": self.transport,
            "canonical_identity": self.canonical_identity,
        }


def _strip_git_suffix(value: str) -> str:
    return value[:-4] if value.endswith(".git") else value


def parse_repository_identity(remote_url: str) -> RepositoryIdentity:
    """Parse a Git remote URL into an exact canonical repository identity."""

    raw = str(remote_url or "").strip()
    if not raw:
        raise RepositoryIdentityError("repository remote URL is empty")
    if "?" in raw or "#" in raw:
        raise RepositoryIdentityError("repository remote URL must not contain query or fragment")

    transport = ""
    host = ""
    owner = ""
    repository = ""

    if raw.startswith("git@"):
        transport = "ssh"
        try:
            host_part, path_part = raw[4:].split(":", 1)
        except ValueError as exc:
            raise RepositoryIdentityError("scp-style git remote must include host:path") from exc
        host = host_part.lower()
        parts = [_strip_git_suffix(part) for part in path_part.strip("/").split("/") if part]
    else:
        parsed = urlparse(raw)
        if parsed.scheme not in {"https", "ssh"}:
            raise RepositoryIdentityError(f"unsupported repository remote transport: {parsed.scheme or 'local'}")
        if parsed.username not in {None, "", "git"}:
            raise RepositoryIdentityError("repository remote URL must not contain non-git userinfo")
        transport = parsed.scheme
        host = (parsed.hostname or "").lower()
        parts = [_strip_git_suffix(part) for part in parsed.path.strip("/").split("/") if part]

    if len(parts) != 2:
        raise RepositoryIdentityError("repository remote must identify exactly owner/repository")
    owner, repository = parts[0].lower(), parts[1].lower()
    if not host or not owner or not repository:
        raise RepositoryIdentityError("repository remote is missing host, owner, or repository")
    canonical = f"{host}/{owner}/{repository}"
    return RepositoryIdentity(
        host=host,
        owner=owner,
        repository=repository,
        transport=transport,
        canonical_identity=canonical,
    )


def assert_expected_repository_identity(
    remote_url: str,
    *,
    expected_identity: str = DEFAULT_DOMINIUM_IDENTITY,
) -> RepositoryIdentity:
    parsed = parse_repository_identity(remote_url)
    expected = expected_identity.lower().removesuffix(".git").strip("/")
    if parsed.canonical_identity != expected:
        raise RepositoryIdentityError(
            f"unexpected repository identity: {parsed.canonical_identity}; expected {expected}"
        )
    return parsed
