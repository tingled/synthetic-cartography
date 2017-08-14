.PHONY : lint test build-container all

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environmental variable $* not set" && exit 1; \
	fi

build-container : guard-DOCKER_IMG
	docker build -t $(DOCKER_IMG) ./

lint :
	flake8 feature_extraction tests

test : lint
	docker run --rm -i -v ${PWD}:/home -w /home $(DOCKER_IMG) nosetests tests

all : build-container test
