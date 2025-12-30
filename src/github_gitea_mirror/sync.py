"""Core synchronization logic."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from github_gitea_mirror.gitea import GiteaClient
from github_gitea_mirror.github import GitHubClient

if TYPE_CHECKING:
    from github_gitea_mirror.config import Config

logger = logging.getLogger(__name__)


def sync_once(config: Config) -> tuple[int, int]:
    """Run a single synchronization pass.

    Args:
        config: Application configuration.

    Returns:
        Tuple of (new_repos_found, successfully_mirrored).
    """
    logger.info("=" * 50)
    logger.info("Starting sync check...")

    with GitHubClient(config.github_token) as github:
        username = github.get_username()
        logger.info("GitHub user: %s", username)

        github_repos = list(
            github.iter_repos(
                include_private=config.include_private,
                include_forks=config.include_forks,
            )
        )
        logger.info("GitHub repos: %d", len(github_repos))

    with GiteaClient(config.gitea_url, config.gitea_token) as gitea:
        existing = gitea.get_repo_names(config.gitea_owner)
        logger.info("Gitea existing repos: %d", len(existing))

        # Find new repos
        new_repos = [
            r for r in github_repos if r.name not in existing and r.name not in config.skip_repos
        ]

        if not new_repos:
            logger.info("No new repos to mirror")
            return 0, 0

        logger.info("Found %d new repos to mirror", len(new_repos))

        if config.dry_run:
            for repo in new_repos:
                logger.info("  [DRY-RUN] Would mirror: %s", repo.name)
            return len(new_repos), 0

        # Create mirrors
        success = 0
        for repo in new_repos:
            if gitea.create_mirror(repo, config.gitea_owner, config.github_token, config):
                success += 1
            time.sleep(1)  # Rate limiting

        logger.info("Sync complete: %d/%d successful", success, len(new_repos))
        return len(new_repos), success


def run_daemon(config: Config) -> None:
    """Run continuous synchronization.

    Args:
        config: Application configuration.
    """
    logger.info("Starting daemon mode (interval: %ds)", config.sync_interval)

    while True:
        try:
            sync_once(config)
        except Exception:
            logger.exception("Error during sync")

        logger.info("Next check in %d seconds...", config.sync_interval)
        time.sleep(config.sync_interval)
