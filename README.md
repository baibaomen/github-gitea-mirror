<p align="center">
  <h1 align="center">🪞 GitHub Gitea Mirror</h1>
  <p align="center">
    <strong>Automatically discover and mirror your entire GitHub account to your self-hosted Gitea.</strong>
  </p>
  <p align="center">
    <a href="https://github.com/baibaomen/github-gitea-mirror/releases"><img src="https://img.shields.io/github/v/release/baibaomen/github-gitea-mirror?style=flat-square" alt="Release"></a>
    <a href="https://github.com/baibaomen/github-gitea-mirror/actions"><img src="https://img.shields.io/github/actions/workflow/status/baibaomen/github-gitea-mirror/ci.yml?style=flat-square" alt="CI"></a>
    <a href="https://pypi.org/project/github-gitea-mirror/"><img src="https://img.shields.io/pypi/v/github-gitea-mirror?style=flat-square" alt="PyPI"></a>
    <a href="https://hub.docker.com/r/baibaomen/github-gitea-mirror"><img src="https://img.shields.io/docker/pulls/baibaomen/github-gitea-mirror?style=flat-square" alt="Docker"></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/baibaomen/github-gitea-mirror?style=flat-square" alt="License"></a>
  </p>
  <p align="center">
    <a href="README.zh-CN.md">🇨🇳 中文文档</a>
  </p>
</p>

---

Set it once, and every new repo you create on GitHub will be automatically mirrored to your Gitea. No manual clicks. No forgotten backups. Just peace of mind. 🍵

## ⚡ Quick Start

Choose your preferred method — all take under 5 minutes:

### 🐳 Docker (Recommended)

```bash
docker run -d --name github-gitea-mirror \
  -e GITHUB_TOKEN=ghp_xxxx \
  -e GITEA_URL=https://your-gitea.com \
  -e GITEA_TOKEN=your_gitea_token \
  -e GITEA_OWNER=your_username \
  --restart unless-stopped \
  baibaomen/github-gitea-mirror
```

Done! It will check for new repos every 10 minutes.

### 📦 PyPI

```bash
pip install github-gitea-mirror

# Run once
github-gitea-mirror --github-token ghp_xxxx --gitea-url https://your-gitea.com --gitea-token xxxx --gitea-owner you

# Or run as daemon
github-gitea-mirror --daemon --interval 600
```

### 🤖 GitHub Action (Zero Infrastructure)

Add to `.github/workflows/mirror.yml` in any of your repos:

```yaml
name: Mirror to Gitea
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:

jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: baibaomen/github-gitea-mirror@master
        with:
          github_token: ${{ secrets.GH_PAT }}
          gitea_url: https://your-gitea.com
          gitea_token: ${{ secrets.GITEA_TOKEN }}
          gitea_owner: your_username
```

---

## ✨ Features

- 🔍 **Auto-discovery** — Detects new repos in your GitHub account automatically
- 🪞 **True mirror** — Creates Gitea mirror repos that sync on schedule
- 🔒 **Private repos** — Supports private repositories (with proper token scopes)
- 🍴 **Fork control** — Choose whether to include forked repos
- ⏰ **Configurable** — Set your own check interval and mirror frequency
- 🐳 **Multiple deployment options** — Docker, PyPI, GitHub Action
- 📝 **Dry-run mode** — Preview what would be mirrored without making changes

---

## ⚙️ Configuration

| Environment Variable | CLI Flag | Required | Default | Description |
|---------------------|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | `--github-token` | ✅ | - | GitHub PAT with `repo` scope |
| `GITEA_URL` | `--gitea-url` | ✅ | - | Your Gitea instance URL |
| `GITEA_TOKEN` | `--gitea-token` | ✅ | - | Gitea access token |
| `GITEA_OWNER` | `--gitea-owner` | ✅ | - | Gitea user/org to own mirrors |
| `SYNC_INTERVAL` | `--interval` | ❌ | `600` | Seconds between checks |
| `MIRROR_INTERVAL` | `--mirror-interval` | ❌ | `10m` | Gitea's sync frequency |
| `INCLUDE_PRIVATE` | `--include-private` | ❌ | `true` | Mirror private repos |
| `INCLUDE_FORKS` | `--include-forks` | ❌ | `false` | Mirror forked repos |
| `SKIP_REPOS` | `--skip` | ❌ | - | Comma-separated repos to skip |
| `DRY_RUN` | `--dry-run` | ❌ | `false` | Preview without changes |

### Token Permissions

**GitHub PAT** needs:
- `repo` (for private repos) or `public_repo` (public only)

**Gitea Token** needs:
- `repo` permission

---

## 🐳 Docker Compose

For persistent deployment:

```yaml
services:
  mirror:
    image: baibaomen/github-gitea-mirror
    restart: unless-stopped
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITEA_URL=${GITEA_URL}
      - GITEA_TOKEN=${GITEA_TOKEN}
      - GITEA_OWNER=${GITEA_OWNER}
      - SYNC_INTERVAL=600
      - INCLUDE_FORKS=false
```

---

## 🛠️ Development

```bash
git clone https://github.com/baibaomen/github-gitea-mirror
cd github-gitea-mirror
pip install -e ".[dev]"

# Run tests
pytest

# Lint & format
ruff check --fix .
ruff format .

# Type check
mypy src
```

---

## 📋 Roadmap

- [x] GitHub → Gitea one-way mirror
- [ ] Gitea → GitHub sync (bidirectional)
- [ ] GitLab support
- [ ] Web UI dashboard
- [ ] Webhook-triggered instant sync

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

## 📄 License

[MIT](LICENSE) — use it however you like.

---

<p align="center">
  <sub>If this saves you time, a ⭐ helps others discover it too!</sub>
</p>
