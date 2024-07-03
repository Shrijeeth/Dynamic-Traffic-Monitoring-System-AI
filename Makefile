install:
	python -m pip install -r requirements.txt

lint:
	python -m pylint $(shell git ls-files '*.py')

auto-lint:
	python -m black --safe $(shell git ls-files --modified --others '*.py')

run:
	python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	ENVIRONMENT=test python -m pytest -v -p no:warnings

test-report:
	ENVIRONMENT=test python -m pytest -v -p no:warnings --cov=. --cov-report=html:coverage
