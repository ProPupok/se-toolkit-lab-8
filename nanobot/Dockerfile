FROM astral/uv:python3.14-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml ./
RUN uv lock && uv sync --frozen
COPY . ./nanobot/
FROM python:3.14.2-slim-bookworm
RUN groupadd --gid 1000 nonroot && useradd --gid 1000 --uid 1000 --create-home nonroot
COPY --from=builder --chown=nonroot:nonroot /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
RUN chown -R nonroot:nonroot /app/nanobot/workspace
USER nonroot
CMD ["python", "/app/nanobot/entrypoint.py"]
