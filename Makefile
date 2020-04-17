.PHONY : lint test build

lint :
	flake8 cartography/ tests/ bin/

type-check:
	mypy cartography/ tests/ bin

build :
	docker build -t carto ./

test : lint type-check
	nosetests tests
