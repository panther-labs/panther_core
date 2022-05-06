packages = panther_core

ci: unit

deps:
	pip install -r requirements.txt

unit:
	python -m unittest discover -s ./tests/unit/panther_core/

test: unit
