"""Configuration management."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration.

    Attributes:
        github_token: GitHub Personal Access Token.
        gitea_url: Gitea instance URL.
        gitea_token: Gitea access token.
        gitea_owner: Gitea user/org to own mirrored repos.
        sync_interval: Seconds between sync checks.
        mirror_interval: Gitea mirror sync interval (e.g., "10m").
        include_private: Whether to mirror private repos.
        include_forks: Whether to mirror forked repos.
        skip_repos: Set of repository names to skip.
        dry_run: If True, only preview without making changes.
    """

    github_token: str
    gitea_url: str
    gitea_token: str
    gitea_owner: str
    sync_interval: int = 600
    mirror_interval: str = "10m"
    include_private: bool = True
    include_forks: bool = False
    skip_repos: set[str] = field(default_factory=set)
    dry_run: bool = False

    @classmethod
    def from_env(cls) -> Config:
        """Create config from environment variables.

        Returns:
            Config instance populated from environment.

        Raises:
            ValueError: If required environment variables are missing.
        """
        missing = []
        github_token = os.environ.get("GITHUB_TOKEN", "")
        gitea_url = os.environ.get("GITEA_URL", "")
        gitea_token = os.environ.get("GITEA_TOKEN", "")
        gitea_owner = os.environ.get("GITEA_OWNER", "")

        if not github_token:
            missing.append("GITHUB_TOKEN")
        if not gitea_url:
            missing.append("GITEA_URL")
        if not gitea_token:
            missing.append("GITEA_TOKEN")
        if not gitea_owner:
            missing.append("GITEA_OWNER")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        skip_repos_str = os.environ.get("SKIP_REPOS", "")
        skip_repos = set(filter(None, skip_repos_str.split(",")))

        return cls(
            github_token=github_token,
            gitea_url=gitea_url.rstrip("/"),
            gitea_token=gitea_token,
            gitea_owner=gitea_owner,
            sync_interval=int(os.environ.get("SYNC_INTERVAL", "600")),
            mirror_interval=os.environ.get("MIRROR_INTERVAL", "10m"),
            include_private=os.environ.get("INCLUDE_PRIVATE", "true").lower() == "true",
            include_forks=os.environ.get("INCLUDE_FORKS", "false").lower() == "true",
            skip_repos=skip_repos,
            dry_run=os.environ.get("DRY_RUN", "false").lower() == "true",
        )
