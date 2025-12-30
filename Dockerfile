FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir build && \
    python -m build --wheel

FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/nickelchen/github-gitea-mirror"
LABEL org.opencontainers.image.description="Automatically mirror GitHub repos to Gitea"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl && rm *.whl

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["github-gitea-mirror"]
CMD ["--daemon"]
