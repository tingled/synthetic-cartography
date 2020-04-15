.PHONY : lint test build

lint :
	flake8 cartography/ tests/

build :
	docker build -t carto ./

test : lint
	nosetests tests
