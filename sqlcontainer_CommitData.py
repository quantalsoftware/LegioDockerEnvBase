#!/usr/bin/env python
import os
import sys
import warnings
import datetime
import gc
import numpy as np
import pandas as pd
import mysql.connector as mysql
import pickle
import boto3

#dbHostContainer = "ec2-13-239-132-26.ap-southeast-2.compute.amazonaws.com"
# dbHostContainer = "172.50.0.20"
# dbHostPort = "31330"
dbHostContainer = "localhost"
dbHostPort = "3306"
user = "root"
passwd = "root"

session = boto3.Session(
    aws_access_key_id='AKIA2Y4DCQESHJLWI4YR',
    aws_secret_access_key='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',
)
s3 = session.resource('s3')
s3bucketName = 'legio-data'
bucket = s3.Bucket(name=s3bucketName)
bucket.download_file("BaseConfigInfo.csv", "BaseConfigInfo.csv")
baseConfigData = pd.read_csv("BaseConfigInfo.csv")

database = mysql.connect(host=dbHostContainer,port=dbHostPort,user=user,passwd=passwd)
dbConnection = database.cursor()
dbConnection.execute("SHOW DATABASES")
databasesRaw = dbConnection.fetchall()  
databases =[]
for i in range(len(databasesRaw)):
    databases.append(databasesRaw[i][0])

for index, row in baseConfigData.loc[baseConfigData['ActiveTrading']==True].iterrows():
    if row['Symbol'] not in databases:
        database = mysql.connect(host=dbHostContainer,port=dbHostPort,user=user,passwd=passwd)
        dbConnection = database.cursor()
        dbConnection.execute("CREATE DATABASE "+row['Symbol'])

        database = mysql.connect(host=dbHostContainer,port=dbHostPort,user=user,passwd=passwd,database=baseCode)
        dbConnection = database.cursor()
        dbConnection.execute("CREATE TABLE "+baseCode+"_Hour (Timestamp VARCHAR(255), Open VARCHAR(10), High VARCHAR(10), Low VARCHAR(10), Close VARCHAR(10))")

        database = mysql.connect(host=dbHostContainer,port=dbHostPort,user=user,passwd=passwd,database=baseCode)
        dbConnection = database.cursor()
        dbConnection.execute("CREATE TABLE "+baseCode+"_Min (Timestamp VARCHAR(255), Open VARCHAR(10), High VARCHAR(10), Low VARCHAR(10), Close VARCHAR(10), Vol VARCHAR(255))")


for index, row in baseConfigData.loc[baseConfigData['ActiveTrading']==True].iterrows():
    hours = []
    baseCode = row['Symbol']    
    for file in os.listdir("data/"):
        if baseCode+"_hour" in file:
            pickle_in = open('data/'+file,'rb')
            hours = hours + np.array(pickle.load(pickle_in)).tolist()
            
    hourDF = pd.DataFrame(hours,columns=['Timestamp', 'Open', 'High', 'Low', 'Close'])
    hourDF = hourDF.drop_duplicates('Timestamp', keep='first').sort_values('Timestamp').reset_index(drop=True)
    hourDF['Timestamp'] = pd.to_datetime(hourDF['Timestamp'])
    hourDF = hourDF.loc[hourDF['Timestamp'] > datetime.datetime(2013,12,31,23,0)].reset_index(drop=True)
    hourDF['Timestamp'] = hourDF['Timestamp'].astype(str)# .strftime("%Y-%m-%d %H:%M:%S")

    for commitData in list(np.array_split(hourDF,2500)):
        vals = [tuple(x) for x in commitData.values]
        sql = "INSERT INTO "+baseCode+"_Hour (Timestamp, Open, High, Low, Close) VALUES (%s, %s, %s, %s, %s)"
        database = mysql.connect(host=dbHostContainer,port=dbHostPort,user=user,passwd=passwd,database=baseCode)
        dbConnection = database.cursor()
        dbConnection.executemany(sql, vals)
        database.commit()
    print(row['Symbol']+" Hourly Data Loaded")
    gc.collect()
    
    mins = []
    baseCode = row['Symbol']    
    for file in os.listdir("data/"):
        if baseCode+"_min" in file:
            pickle_in = open('data/'+file,'rb')
            mins = mins + np.array(pickle.load(pickle_in)).tolist()
            
    minDF = pd.DataFrame(mins,columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Vol'])
    minDF = minDF.drop_duplicates('Timestamp', keep='first').sort_values('Timestamp').reset_index(drop=True)
    minDF['Timestamp'] = pd.to_datetime(minDF['Timestamp'])
    minDF = minDF.loc[minDF['Timestamp'] > datetime.datetime(2013,12,31,23,0)].reset_index(drop=True)
    minDF['Timestamp'] = minDF['Timestamp'].astype(str)# .strftime("%Y-%m-%d %H:%M:%S")
    
    for commitData in list(np.array_split(minDF,25000)):
        vals = [tuple(x) for x in commitData.values]
        sql = "INSERT INTO "+baseCode+"_Min (Timestamp, Open, High, Low, Close, Vol) VALUES (%s, %s, %s, %s, %s, %s)"
        database = mysql.connect(host=dbHostContainer,port=dbHostPort,user=user,passwd=passwd,database=baseCode)
        dbConnection = database.cursor()
        dbConnection.executemany(sql, vals)
        database.commit()
    print(row['Symbol']+" Min Data Loaded")
    print()

exit()