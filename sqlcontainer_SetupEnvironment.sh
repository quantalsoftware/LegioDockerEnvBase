#!/bin/sh
set -e

apt update
apt install nano
apt install python3-pip
pip3 install pandas
pip3 install mysql-connector-python
pip3 install boto3
pip3 install awscli