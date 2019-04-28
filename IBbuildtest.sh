#!/bin/sh
set -e

echo "Load IB Docker"
for i in 5050 5051
do
    sudo docker build --build-arg $i -t legioib$i -f ./DockerfileIB .
done
