"""Command-line interface."""

from __future__ import annotations

import logging
from importlib.metadata import version
from typing import Annotated

import typer

from github_gitea_mirror.config import Config
from github_gitea_mirror.sync import run_daemon, sync_once

__version__ = version("github-gitea-mirror")


def version_callback(value: bool) -> None:
    if value:
        print(f"github-gitea-mirror {__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="github-gitea-mirror",
    help="Automatically mirror your GitHub repos to Gitea.",
    add_completion=False,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    github_token: Annotated[
        str | None, typer.Option(envvar="GITHUB_TOKEN", help="GitHub PAT")
    ] = None,
    gitea_url: Annotated[str | None, typer.Option(envvar="GITEA_URL", help="Gitea URL")] = None,
    gitea_token: Annotated[
        str | None, typer.Option(envvar="GITEA_TOKEN", help="Gitea token")
    ] = None,
    gitea_owner: Annotated[
        str | None, typer.Option(envvar="GITEA_OWNER", help="Gitea owner")
    ] = None,
    interval: Annotated[
        int, typer.Option(envvar="SYNC_INTERVAL", help="Sync interval in seconds")
    ] = 600,
    mirror_interval: Annotated[
        str, typer.Option(envvar="MIRROR_INTERVAL", help="Gitea mirror interval")
    ] = "10m",
    include_private: Annotated[bool, typer.Option(help="Include private repos")] = True,
    include_forks: Annotated[bool, typer.Option(help="Include forked repos")] = False,
    skip: Annotated[str | None, typer.Option(help="Repos to skip (comma-separated)")] = None,
    dry_run: Annotated[bool, typer.Option(help="Preview without changes")] = False,
    daemon: Annotated[bool, typer.Option(help="Run continuously")] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version", "-v", callback=version_callback, is_eager=True, help="Show version"
        ),
    ] = False,
) -> None:
    """Mirror GitHub repositories to Gitea."""
    # Validate required args
    missing = []
    if not github_token:
        missing.append("--github-token or GITHUB_TOKEN")
    if not gitea_url:
        missing.append("--gitea-url or GITEA_URL")
    if not gitea_token:
        missing.append("--gitea-token or GITEA_TOKEN")
    if not gitea_owner:
        missing.append("--gitea-owner or GITEA_OWNER")

    if missing:
        typer.echo(f"Error: Missing required options: {', '.join(missing)}", err=True)
        typer.echo("Run with --help for usage information.", err=True)
        raise typer.Exit(1)

    config = Config(
        github_token=github_token,  # type: ignore[arg-type]
        gitea_url=gitea_url,  # type: ignore[arg-type]
        gitea_token=gitea_token,  # type: ignore[arg-type]
        gitea_owner=gitea_owner,  # type: ignore[arg-type]
        sync_interval=interval,
        mirror_interval=mirror_interval,
        include_private=include_private,
        include_forks=include_forks,
        skip_repos=set(filter(None, (skip or "").split(","))),
        dry_run=dry_run,
    )

    if daemon:
        run_daemon(config)
    else:
        sync_once(config)


if __name__ == "__main__":
    app()
