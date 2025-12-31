<p align="center">
  <h1 align="center">🪞 GitHub Gitea Mirror</h1>
  <p align="center">
    <strong>自动发现并镜像你整个 GitHub 账号的仓库到自建的 Gitea。</strong>
  </p>
  <p align="center">
    <a href="https://github.com/baibaomen/github-gitea-mirror/releases"><img src="https://img.shields.io/github/v/release/baibaomen/github-gitea-mirror?style=flat-square" alt="Release"></a>
    <a href="https://github.com/baibaomen/github-gitea-mirror/actions"><img src="https://img.shields.io/github/actions/workflow/status/baibaomen/github-gitea-mirror/ci.yml?style=flat-square" alt="CI"></a>
    <a href="https://pypi.org/project/github-gitea-mirror/"><img src="https://img.shields.io/pypi/v/github-gitea-mirror?style=flat-square" alt="PyPI"></a>
    <a href="https://github.com/baibaomen/github-gitea-mirror/pkgs/container/github-gitea-mirror"><img src="https://img.shields.io/badge/docker-ghcr.io-blue?style=flat-square" alt="Docker"></a>
    <a href="LICENSE"><img src="https://img.shields.io/github/license/baibaomen/github-gitea-mirror?style=flat-square" alt="License"></a>
  </p>
  <p align="center">
    <a href="README.md">🇺🇸 English</a>
  </p>
</p>

---

配置一次，从此你在 GitHub 新建的每个仓库都会自动镜像到 Gitea。无需手动操作，无需担心遗漏。安心喝茶 🍵

## ⚡ 快速开始

任选一种方式，5 分钟内即可运行：

### 🐳 Docker（推荐）

```bash
docker run -d --name github-gitea-mirror \
  -e GITHUB_TOKEN=ghp_xxxx \
  -e GITEA_URL=https://your-gitea.com \
  -e GITEA_TOKEN=your_gitea_token \
  -e GITEA_OWNER=your_username \
  --restart unless-stopped \
  ghcr.io/baibaomen/github-gitea-mirror
```

完成！默认每 10 分钟检查一次新仓库。

### 📦 PyPI

```bash
pip install github-gitea-mirror

# 运行一次
github-gitea-mirror --github-token ghp_xxxx --gitea-url https://your-gitea.com --gitea-token xxxx --gitea-owner you

# 或作为守护进程运行
github-gitea-mirror --daemon --interval 600
```

### 🤖 GitHub Action（零基础设施）

在你的任意仓库添加 `.github/workflows/mirror.yml`：

```yaml
name: Mirror to Gitea
on:
  schedule:
    - cron: '0 * * * *'  # 每小时
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

## ✨ 功能特性

- 🔍 **自动发现** — 自动检测 GitHub 账号下的新仓库
- 🪞 **真正镜像** — 创建的 Gitea 镜像仓库会按计划自动同步
- 🔒 **私有仓库** — 支持同步私有仓库（需要相应 Token 权限）
- 🍴 **Fork 控制** — 可选择是否包含 fork 的仓库
- ⏰ **可配置** — 自定义检查间隔和镜像同步频率
- 🐳 **多种部署** — Docker、PyPI、GitHub Action 任选
- 📝 **预览模式** — 先看会同步什么，再决定是否执行

---

## ⚙️ 配置项

| 环境变量 | CLI 参数 | 必填 | 默认值 | 说明 |
|---------|---------|------|--------|------|
| `GITHUB_TOKEN` | `--github-token` | ✅ | - | GitHub PAT，需 `repo` 权限 |
| `GITEA_URL` | `--gitea-url` | ✅ | - | Gitea 地址 |
| `GITEA_TOKEN` | `--gitea-token` | ✅ | - | Gitea 访问令牌 |
| `GITEA_OWNER` | `--gitea-owner` | ✅ | - | Gitea 中存放镜像的用户/组织 |
| `SYNC_INTERVAL` | `--interval` | ❌ | `600` | 检查间隔（秒） |
| `MIRROR_INTERVAL` | `--mirror-interval` | ❌ | `10m` | Gitea 镜像同步频率 |
| `INCLUDE_PRIVATE` | `--include-private` | ❌ | `true` | 是否同步私有仓库 |
| `INCLUDE_FORKS` | `--include-forks` | ❌ | `false` | 是否同步 fork 仓库 |
| `SKIP_REPOS` | `--skip` | ❌ | - | 跳过的仓库（逗号分隔） |
| `DRY_RUN` | `--dry-run` | ❌ | `false` | 预览模式 |

### Token 权限

**GitHub PAT** 需要：
- `repo`（同步私有仓库）或 `public_repo`（仅公开仓库）

**Gitea Token** 需要：
- `repo` 权限

---

## 🐳 Docker Compose

持久化部署：

```yaml
services:
  mirror:
    image: ghcr.io/baibaomen/github-gitea-mirror
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

## 🛠️ 开发

```bash
git clone https://github.com/baibaomen/github-gitea-mirror
cd github-gitea-mirror
pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查和格式化
ruff check --fix .
ruff format .

# 类型检查
mypy src
```

---

## 📋 路线图

- [x] GitHub → Gitea 单向镜像
- [ ] 双向同步
- [ ] GitLab 支持
- [ ] Web 管理界面
- [ ] Webhook 实时同步

---

## 🤝 贡献

欢迎贡献代码！请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 开源协议

[MIT](LICENSE) — 随意使用。

---

<p align="center">
  <sub>如果这个工具帮到了你，点个 ⭐ 让更多人发现它！</sub>
</p>
