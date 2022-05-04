packages = panther_core

ci: unit

deps:
	pipenv install --dev

unit:
	pipenv run nosetests -v

test: unit
