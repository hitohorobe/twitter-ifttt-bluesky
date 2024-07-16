FROM public.ecr.aws/docker/library/python:3.11.9-slim AS local

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl

COPY . . 

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_NO_INTERACTION=1

RUN poetry config virtualenvs.create false --local
RUN poetry install

EXPOSE 8080


# for release
FROM local AS render

RUN poetry install --only main
EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]