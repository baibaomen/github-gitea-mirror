"""Tests for configuration module."""

import os
from unittest import mock

import pytest

from github_gitea_mirror.config import Config


class TestConfig:
    """Tests for Config class."""

    def test_from_env_with_all_required(self) -> None:
        """Test creating config with all required env vars."""
        env = {
            "GITHUB_TOKEN": "ghp_test",
            "GITEA_URL": "https://gitea.example.com",
            "GITEA_TOKEN": "gitea_token",
            "GITEA_OWNER": "testuser",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            config = Config.from_env()

        assert config.github_token == "ghp_test"
        assert config.gitea_url == "https://gitea.example.com"
        assert config.gitea_token == "gitea_token"
        assert config.gitea_owner == "testuser"
        assert config.sync_interval == 600
        assert config.mirror_interval == "10m"
        assert config.include_private is True
        assert config.include_forks is False

    def test_from_env_missing_required(self) -> None:
        """Test that missing required vars raise ValueError."""
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Missing required"):
                Config.from_env()

    def test_from_env_with_optional(self) -> None:
        """Test creating config with optional env vars."""
        env = {
            "GITHUB_TOKEN": "ghp_test",
            "GITEA_URL": "https://gitea.example.com/",
            "GITEA_TOKEN": "gitea_token",
            "GITEA_OWNER": "testuser",
            "SYNC_INTERVAL": "300",
            "MIRROR_INTERVAL": "5m",
            "INCLUDE_PRIVATE": "false",
            "INCLUDE_FORKS": "true",
            "SKIP_REPOS": "repo1,repo2",
            "DRY_RUN": "true",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            config = Config.from_env()

        assert config.gitea_url == "https://gitea.example.com"  # trailing slash stripped
        assert config.sync_interval == 300
        assert config.mirror_interval == "5m"
        assert config.include_private is False
        assert config.include_forks is True
        assert config.skip_repos == {"repo1", "repo2"}
        assert config.dry_run is True

    def test_skip_repos_empty(self) -> None:
        """Test empty skip_repos."""
        env = {
            "GITHUB_TOKEN": "ghp_test",
            "GITEA_URL": "https://gitea.example.com",
            "GITEA_TOKEN": "gitea_token",
            "GITEA_OWNER": "testuser",
            "SKIP_REPOS": "",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            config = Config.from_env()

        assert config.skip_repos == set()
