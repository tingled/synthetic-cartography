.PHONY : lint test

lint :
	flake8 cartography/

test : lint
