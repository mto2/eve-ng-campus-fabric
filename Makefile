SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help
.PHONY: help ansible apply backup bootstrap build config shell netbox-get

DOCKER_IMG = packetferret/ansible-vxlan-evpn-for-campus
DOCKER_TAG = 0.0.2

help:
	@echo ''
	@echo 'Makefile will help us build with the following commands'
	@echo '		make ansible				builds the configuration and applies them to the network devices'
	@echo '		make apply				will apply the generated config to the network devices'
	@echo '		make build				build the container image'
	@echo '		make config				will only build the configurations, will not push to devices'

ansible: config apply

apply:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-v $(PWD)/files/tmp:/tmp \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.configuration.apply.yml 

backup:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-v $(PWD)/files/tmp:/tmp \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.configuration.backup.yml 

bootstrap:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-v $(PWD)/files/tmp:/tmp \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.configuration.bootstrap.yml 

build:
	docker build -t $(DOCKER_IMG):$(DOCKER_TAG) files/docker/ansible/

config:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-v $(PWD)/files/tmp:/tmp \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.configuration.build.yml

netbox-get:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-v $(PWD)/files/tmp:/tmp \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.netbox.retrieve.info.yml

shell:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-v $(PWD)/files/tmp:/tmp \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) /bin/sh

