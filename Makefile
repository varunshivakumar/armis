#vars
IMAGE_TAG=collector

dependencies: 
		pipenv run pip freeze > requirements.txt

clean: 
		docker image rm ${IMAGE_TAG}

build: dependencies
	    docker build -t ${IMAGE_TAG} .

push:
	    docker push ${IMAGE_TAG}

run: build
		 docker run -it -m 512m --memory-reservation=256m ${IMAGE_TAG}

all: clean build run