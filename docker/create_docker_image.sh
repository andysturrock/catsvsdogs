#!/bin/bash

pushd .
cd ..

docker build -f docker/Dockerfile -t cats-vs-dogs-model .

docker tag cats-vs-dogs-model:latest 089953642441.dkr.ecr.eu-west-1.amazonaws.com/cats-vs-dogs-model:latest

aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 089953642441.dkr.ecr.eu-west-1.amazonaws.com

docker push 089953642441.dkr.ecr.eu-west-1.amazonaws.com/cats-vs-dogs-model:latest

popd
