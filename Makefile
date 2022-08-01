packages = panther_core

ci: lint test


deps:
	pipenv install --dev

deps-update:
	pipenv update
	pipenv lock -r  > requirements.txt

lint:
	pipenv run mypy $(packages) --disallow-untyped-defs --ignore-missing-imports --warn-unused-ignores
	pipenv run bandit -r $(packages)
	pipenv run pylint $(packages) --disable=missing-docstring,bad-continuation,duplicate-code,W0511,R0912,too-many-lines --max-line-length=100

fmt:
	pipenv run isort --profile=black $(packages)
	pipenv run black --line-length=100 $(packages)

install:
	pipenv install --dev
	pipenv lock -r  > requirements.txt

package: install
	pipenv run python3 setup.py sdist

publish: install package
	twine upload dist/*

test:
	pipenv run nosetests -v
