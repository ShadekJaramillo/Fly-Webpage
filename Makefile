run_api_mock:
	export $$(grep '^API_PORT=' .env | xargs) && uv run --directory backend fastapi dev src/db_api/main.py --port $$API_PORT