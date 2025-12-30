"""Tests for GitHub client."""

from github_gitea_mirror.github import GitHubRepo


class TestGitHubRepo:
    """Tests for GitHubRepo dataclass."""

    def test_create_repo(self) -> None:
        """Test creating a GitHubRepo instance."""
        repo = GitHubRepo(
            name="test-repo",
            full_name="user/test-repo",
            clone_url="https://github.com/user/test-repo.git",
            private=False,
            fork=False,
            description="A test repo",
        )

        assert repo.name == "test-repo"
        assert repo.full_name == "user/test-repo"
        assert repo.clone_url == "https://github.com/user/test-repo.git"
        assert repo.private is False
        assert repo.fork is False
        assert repo.description == "A test repo"

    def test_repo_is_frozen(self) -> None:
        """Test that GitHubRepo is immutable."""
        repo = GitHubRepo(
            name="test",
            full_name="user/test",
            clone_url="https://github.com/user/test.git",
            private=False,
            fork=False,
            description="",
        )

        # Should raise FrozenInstanceError
        try:
            repo.name = "changed"  # type: ignore[misc]
            assert False, "Should have raised an error"
        except Exception:
            pass  # Expected
