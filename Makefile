SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help
.PHONY: help ansible apply build config

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
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.configuration.apply.yml 

build:
	docker build -t $(DOCKER_IMG):$(DOCKER_TAG) files/docker/ansible/

config:
	docker run -it \
	--rm \
	-v $(PWD)/files/:/home/tmp/files \
	-w /home/tmp/files/ansible/ \
	$(DOCKER_IMG):$(DOCKER_TAG) ansible-playbook pb.configuration.build.yml

# ### side note: simplifying by removing local ansible execution
# ### until someone declares that they want it.
# ### will push foward with only docker-based deployments for now

# run:
# 	cd $(PWD)/files/ansible/; \
# 	ansible-playbook pb.configuration.network.yml 
