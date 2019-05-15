#!/usr/bin/env python
import os
import sys
import warnings
import pandas as pd
import mysql.connector as mysql
import pickle
import boto3

#s3 = boto3.resource('s3')
session = boto3.Session(
    aws_access_key_id='AKIA2Y4DCQESHJLWI4YR',
    aws_secret_access_key='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',
)
s3 = session.resource('s3')
s3bucketName = 'legio-data'
bucket = s3.Bucket(name=s3bucketName)
s3_StorageLocation = "database_data/"

localStorage = '/root/data/'
s3Files = [x for x in bucket.objects.filter(Prefix=s3_StorageLocation)]

for file in s3Files:
    if 'mins' in file.key:
        bucket.download_file(file.key, localStorage+str(file.key).split("/")[-1])
    if 'hours' in file.key:
        bucket.download_file(file.key, localStorage+str(file.key).split("/")[-1])
        
exit()