#!/bin/sh
set -e

# IFS=","
# while read f1 f2 f3 f4
# do
#     echo sudo docker run -i -t --name $f1 --net legionet --ip $f3 -d -p $f4:5900 -p 4002:4002 $f2    
# done < "./IBGatewayConfig.csv"


# for i in 5050 5051 5052 5053 5054 5055 5056 5057 5058
# do
#     sudo docker run -i -t 
# done


# echo -n "Press [ENTER] when you have configured gateways through VNC...: "
# read var_name

IFS=","
while read f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12
do
    if [ $f11 = "True" ]
    then
        sudo docker run -i -t --name legiodp_$f2 --net legionet --ip $f9 -d -p $f8:8080 legiodp        
    fi
done < "./BaseConfigInfo.csv"