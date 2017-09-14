.PHONY : lint test build

lint :
	flake8 cartography/

build :
	docker build -t carto ./

test : lint build
	docker run -w /home -v $(CURDIR):/home carto nosetests tests
