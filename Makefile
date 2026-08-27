.PHONY: install validate freshness test schema check

install:
	python -m pip install -e "packages/schemas[dev]"

validate:
	python scripts/validate_corpus.py

freshness:
	python scripts/check_freshness.py

test:
	pytest

schema:
	python packages/schemas/export_json_schema.py

check: validate freshness test
	python packages/schemas/export_json_schema.py --check
