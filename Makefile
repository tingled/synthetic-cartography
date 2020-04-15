.PHONY : lint test build

lint :
	flake8 cartography/

build :
	docker build -t carto ./

test : lint
	nosetests tests
