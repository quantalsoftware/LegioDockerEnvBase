#!/bin/sh
set -e

IFS=","
while read f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12
do
    if [ $f11 = "True" ]
    then
        sudo docker start legiodp_$f2
    fi
done < "./BaseConfigInfo.csv"