"""GitHub API client."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GitHubRepo:
    """GitHub repository information.

    Attributes:
        name: Repository name.
        full_name: Full name (owner/repo).
        clone_url: HTTPS clone URL.
        private: Whether the repo is private.
        fork: Whether the repo is a fork.
        description: Repository description.
    """

    name: str
    full_name: str
    clone_url: str
    private: bool
    fork: bool
    description: str


class GitHubClient:
    """GitHub API client for fetching user repositories."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str) -> None:
        """Initialize the client.

        Args:
            token: GitHub Personal Access Token.
        """
        self._client = httpx.Client(
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "github-gitea-mirror",
            },
            timeout=30.0,
        )

    def get_username(self) -> str:
        """Get the authenticated user's username.

        Returns:
            GitHub username.

        Raises:
            httpx.HTTPStatusError: If the request fails.
        """
        resp = self._client.get(f"{self.BASE_URL}/user")
        resp.raise_for_status()
        login: str = resp.json()["login"]
        return login

    def iter_repos(
        self,
        *,
        include_private: bool = True,
        include_forks: bool = False,
    ) -> Iterator[GitHubRepo]:
        """Iterate over user's repositories.

        Args:
            include_private: Include private repositories.
            include_forks: Include forked repositories.

        Yields:
            GitHubRepo instances.
        """
        page = 1
        per_page = 100

        while True:
            resp = self._client.get(
                f"{self.BASE_URL}/user/repos",
                params={
                    "page": page,
                    "per_page": per_page,
                    "affiliation": "owner",
                    "sort": "updated",
                },
            )
            resp.raise_for_status()
            repos = resp.json()

            if not repos:
                break

            for repo in repos:
                if repo["private"] and not include_private:
                    continue
                if repo["fork"] and not include_forks:
                    continue

                yield GitHubRepo(
                    name=repo["name"],
                    full_name=repo["full_name"],
                    clone_url=repo["clone_url"],
                    private=repo["private"],
                    fork=repo["fork"],
                    description=repo.get("description") or "",
                )

            page += 1

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> GitHubClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
