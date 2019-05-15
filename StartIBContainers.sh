#!/bin/sh
set -e

echo "Start IB Container"
for i in 5050 5051 5052 5053 5054 5055 5056 5057 5058
do
    sudo docker start IBGW$i
done
