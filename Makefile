.PHONY: install validate test schema check

install:
	python -m pip install -e "packages/schemas[dev]"

validate:
	python scripts/validate_corpus.py

test:
	pytest

schema:
	python packages/schemas/export_json_schema.py

check: validate test
	python packages/schemas/export_json_schema.py --check
