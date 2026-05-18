FROM public.ecr.aws/docker/library/python:3.13.2-slim AS local

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/

COPY . .

RUN uv sync --frozen --no-install-project

EXPOSE 8080


# for release
FROM local AS gcloud

RUN uv sync --frozen --no-install-project --no-dev
EXPOSE 8000

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
