VERSION := $(shell cat VERSION)
IMAGE_NAME := dhcalc
ECR_REGISTRY := 128275230365.dkr.ecr.eu-west-2.amazonaws.com

PHONY: build push

build:
	docker build -t ${IMAGE_NAME}:${VERSION} .

push:
	docker tag ${IMAGE_NAME}:${VERSION} ${ECR_REGISTRY}/${IMAGE_NAME}:${VERSION}
	docker tag ${IMAGE_NAME}:${VERSION} ${ECR_REGISTRY}/${IMAGE_NAME}:latest

	docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${VERSION}
	docker push ${ECR_REGISTRY}/${IMAGE_NAME}:latest