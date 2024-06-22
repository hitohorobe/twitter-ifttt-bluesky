CONTAINER_NAME = ifttt_to_bluesky_api


help:
	@echo "Options:"
	@echo "  build:	Build Docker Containers."
	@echo "  up:		Start up app containers in local."
	@echo "  stop:		Stop app containers in local."
	@echo "  lint:		Check style of python files."
	@echo "  format:	Format python files."
	@echo "  test:		Execute pytest in app container."

build:
	@echo "Start Building Containers..."
	@docker compose build

up:
	@echo "Start up app container in local..."
	@docker compose up -d

stop:
	@echo "Stop app container in local..."
	@docker compose stop

lint:
	@echo "Check source code style..."
	@poetry run ruff check .
	@poetry run mypy . --explicit-package-bases --install-types --non-interactive

format:
	@echo "Format source code..."
	@poetry run ruff check . --fix

test:
	@echo "start pytest..."
	@docker compose exec ${CONTAINER_NAME} poetry run pytest tests