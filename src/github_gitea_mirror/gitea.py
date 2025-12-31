"""Gitea API client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from github_gitea_mirror.config import Config
    from github_gitea_mirror.github import GitHubRepo

logger = logging.getLogger(__name__)


class GiteaClient:
    """Gitea API client for managing mirror repositories."""

    def __init__(self, base_url: str, token: str) -> None:
        """Initialize the client.

        Args:
            base_url: Gitea instance URL.
            token: Gitea access token.
        """
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            headers={
                "Authorization": f"token {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=60.0,
        )

    def get_repo_names(self, owner: str) -> set[str]:
        """Get all repository names for an owner.

        Args:
            owner: Username or organization name.

        Returns:
            Set of repository names.
        """
        names: set[str] = set()
        page = 1

        while True:
            resp = self._client.get(
                f"{self.base_url}/api/v1/users/{owner}/repos",
                params={"page": page, "limit": 50},
            )
            resp.raise_for_status()
            repos = resp.json()

            if not repos:
                break

            for repo in repos:
                names.add(repo["name"])
            page += 1

        return names

    def create_mirror(
        self,
        repo: GitHubRepo,
        owner: str,
        github_token: str,
        config: Config,
    ) -> bool:
        """Create a mirror repository in Gitea.

        Args:
            repo: GitHub repository to mirror.
            owner: Gitea owner for the mirror.
            github_token: GitHub token for authenticated clone.
            config: Application configuration.

        Returns:
            True if successful, False otherwise.
        """
        # Build authenticated clone URL (always use oauth2 format for GitHub)
        auth_url = repo.clone_url.replace("https://", f"https://oauth2:{github_token}@")

        payload = {
            "clone_addr": auth_url,
            "repo_name": repo.name,
            "repo_owner": owner,
            "mirror": True,
            "mirror_interval": config.mirror_interval,
            "private": repo.private,
            "description": repo.description,
            "wiki": True,
            "lfs": True,
            "service": "github",
            "auth_token": github_token,  # Required for Gitea to access private repos
        }

        try:
            resp = self._client.post(
                f"{self.base_url}/api/v1/repos/migrate",
                json=payload,
            )

            if resp.status_code in (200, 201):
                logger.info("✅ Created mirror: %s", repo.name)
                return True

            logger.error(
                "❌ Failed to create mirror %s: %s - %s",
                repo.name,
                resp.status_code,
                resp.text,
            )
            return False

        except httpx.HTTPError as e:
            logger.error("❌ HTTP error creating mirror %s: %s", repo.name, e)
            return False

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> GiteaClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
