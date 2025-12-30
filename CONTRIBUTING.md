# Contributing

Thanks for your interest in contributing! 🎉

## Quick Start

1. Fork and clone the repo
2. Install dev dependencies:
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```
3. Create a branch: `git checkout -b feature/my-feature`
4. Make your changes
5. Run checks:
   ```bash
   ruff check .
   ruff format .
   mypy src
   pytest
   ```
6. Commit and push
7. Open a Pull Request

## Code Style

- Use type hints everywhere
- Write docstrings (Google style)
- Keep functions focused and small
- Add tests for new features

## Commit Messages

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance

## Reporting Issues

Please include:
- What you expected
- What actually happened
- Steps to reproduce
- Environment (OS, Python version)

## Code of Conduct

Be kind and respectful. We're all here to learn and improve.
