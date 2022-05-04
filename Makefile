packages = panther_core

ci: lint unit

deps:
	pipenv install --dev

deps-update:
	pipenv update
	pipenv lock -r  > requirements.txt

lint:
	pipenv run mypy $(packages) --disallow-untyped-defs --ignore-missing-imports --warn-unused-ignores
	pipenv run bandit -r $(packages)
	pipenv run pylint $(packages) --disable=missing-docstring,bad-continuation,duplicate-code,W0511,R0912,too-many-lines --max-line-length=100

venv:
	pipenv install --dev

fmt:
	pipenv run isort --profile=black $(packages)
	pipenv run black --line-length=100 $(packages)

install:
	pipenv install --dev

unit:
	pipenv run nosetests -v

test: unit

pypi:
	pipenv run python3 setup.py sdist
	pipenv run twine upload dist/*
