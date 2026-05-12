.PHONY: install lint format test generate scan dashboard health

install:
	python -m pip install -e ".[dev]"

lint:
	ruff check .

format:
	ruff format .

test:
	pytest --cov=src/cloud_audit --cov-report=term-missing --cov-fail-under=85

generate:
	cloud-audit generate-snapshots

scan:
	cloud-audit scan --source snapshots

health:
	cloud-audit health-check

dashboard:
	streamlit run app/streamlit_dashboard.py
