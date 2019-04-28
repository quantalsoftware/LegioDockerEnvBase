#!/bin/sh
set -e

sudo apt update
yes | sudo apt install apt-transport-https ca-certificates curl unzip software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
yes | sudo apt install docker-ce

wget https://github.com/quantalsoftware/LegioDockerEnvBase/archive/master.zip
unzip ./master.zip -d ~/
cd LegioDockerEnvBase-master

outputFile="BaseConfigInfo.csv"
awsFile="BaseConfigInfo.csv"
bucket="legio-data"
bucket="legio-test"
resource="/${bucket}/${awsFile}"
contentType="text/csv"
# Change the content type as desired
dateValue=`TZ=GMT date -R`
#Use dateValue=`date -R` if your TZ is already GMT
stringToSign="GET\n\n${contentType}\n${dateValue}\n${resource}"
s3Key=$1
s3Secret=$2
signature=`echo -n ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -H "Host: ${bucket}.s3.amazonaws.com" \
     -H "Date: ${dateValue}" \
     -H "Content-Type: ${contentType}" \
     -H "Authorization: AWS ${s3Key}:${signature}" \
     https://${bucket}.s3.amazonaws.com/${awsFile} -o $outputFile

cat > credentials << EOL
[default]
aws_access_key_id = $1
aws_secret_access_key = $2
EOL

cat > config << EOL
[default]
region = ap-southeast-2
output = text
EOL

sudo docker network create --subnet=172.50.0.0/16 legionet

# if [ $3 = "SQL" ]
# then
#     ## SQL
#     echo "Load SQL Docker"    
#     sudo docker build -t legiosql -f ./DockerfileSQL .
#     sudo docker run -i -t --name legioSQL --net legionet --ip 172.50.0.20 -d -p 31330:3306 -p 31425:8080 legiosql
#     sudo docker exec -it legioSQL mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION; FLUSH PRIVILEGES;"
# fi


#if [ $3 = "IB" ]
#then
#    IB & DP
    # echo "Load IB Docker"
    # for i in 5050 5051 5052 5053 5054 5055 5056 5057 5058
    # do
    #     echo "sudo docker build --build-arg $1 -t legioib$i -f ./DockerfileIB $i ."
    # done
    