# ANALYSIS OF COVID-19 CASES IN US STATES AND TERRITORIES
This repository contains the information on Analysis of 'COVID-19 cases in US states and territories' data generated through streaming API using Hadoop Components.

## Table of Contents
- [About The Project](#-About-The-Project)
  - [Built With](#Built-With)
- [Getting Started](#Getting-Started)
   - [Installation](#Installation)
   - [Prerequisites](#Prerequisites)
- [Roadmap](#Roadmap)
   - [Data Acquisition](#Data-Acquisition)
   - [Data Ingestion using Kafka](#Data-Ingestion-using-Kafka)
   - [Data Storage](#Data-Storage)
   - [Data Transformation](#Data-Transformation)
   - [Data Visualization](#Data-Visualization)
- [Contact](#Contact)
- [Acknowledgements](#Acknowledgements)

### About The Project
The COVID-19 pandemic is a crisis like no other. It is wise to try and learn from the current situation in China, where the rate of COVID-19 infections was extinguished as a result of a lockdown, and USA, where hospitals are full and doctors have to make life-death decisions about patients. With respect to growing cases in USA, we would like to explore how the data is varying accordingly for US states and territories with various Bigdata technologies.

For this project, the dataset is collected from Data is obtained from COVID-19 Tracking project. States Historical Data API - https://covidtracking.com/api/v1/states/daily.json is being used to retrieve the historical testing data of different US states and territories. The data collected is in JSON format and being updated with the testing data from the month of February to till date for each state. This dataset is available to the public for analysis.

#### Built With
Below are the list of technologies used to accomplish this project.
- Hortonworks HDP - 2.6.5 sandbox from Oracle VM VirtualBox (RAM-8192MB, Processors-4 Core)
- Kafka Server in HDP
- Apache Spark Server in HDP
- Apache Zeppelin in HDP
- MongoDB v3.2.22 in HDP

### Getting Started
- Refer to the video to install Hortonworks HDP - 2.6.5 sandbox from Oracle VM VirtualBox on your desktop/laptop here  https://www.youtube.com/watch?v=735yx2Eak48
- Use Git Clone in HDP Shell to install MongoDB, refer to "https://github.com/nikunjness/mongo-ambari"

#### Installation
- Hortonworks HDP - 2.6.5 sandbox
- MongoDB v3.2.22 in HDP

#### Prerequisites
- Start below services from HDP Sandbox
  - HDFS, YARN service to access hadoop file system
  - HIVEServer2 to create and access tables in HIVE
  - Kafka and Zookeeper to access streaming data
  - Mongo DB server
  - Apache Spark2
  - Apache Zeppelin server for Data Visualization

### Roadmap
#### Data Acquisition
Refer script 'covid19_producer.py' file to extract data from covid-19 streaming public API -https://covidtracking.com/api/v1/states/daily.json.

#### Data Ingestion using Kafka
Kafka topic - 'covid19' is used to consume the data and json response is stored in HDFS file system. Below code is used to perform this action, refer 'covid19_consumer.py' file.

```python
#Kafka Consumer- Consumes the produced data

from kafka import KafkaConsumer

from json import loads,dumps

from subprocess import Popen, PIPE

put = Popen(["hadoop", "fs", "-put", "-", "/user/root/Output.json"],stdin=PIPE, bufsize=-1)

consumer = KafkaConsumer(
        
    'covid19',

     bootstrap_servers='sandbox-hdp.hortonworks.com:6667',

     auto_offset_reset='earliest',

     enable_auto_commit=True,
     
     consumer_timeout_ms = 40000, 
     
     value_deserializer=lambda x: loads(x.decode('utf-8')),

     api_version=(0, 10, 1))

put.stdin.write("[")
for message in consumer:
    message = message.value
    print(dumps(message))
    put.stdin.write(dumps(message))
    put.stdin.write(",")
 
put.stdin.write("{}")
put.stdin.write("]")
put.stdin.close()
put.wait()
```
#### Data Storage
Data on HDFS is loaded on to MongoDB using Apache Sparrk, refer 'hdfs_mongo.py'.

```python
#HDFS-Mongo Used to write the json file from HDFS to Mongo DB

from pyspark.sql import SparkSession

my_spark = SparkSession \
         .builder \
         .appName("MongoDBIntegration") \
         .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/bigdatadb.covid19") \
         .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/bigdatadb.covid19") \
         .getOrCreate()


df = my_spark.read.option("multiline", "true").json("hdfs://sandbox-hdp.hortonworks.com:8020/user/root/Output.json")

df.count()

df.printSchema()

df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("database","bigdatadb").option("collection", "covid19").save()
```

#### Data Transformation
Data is transformed from unstructurred format (Mongo DB- Collection) to structured format (HIVE Tables) using Apache Spark.
```
#Mongo-HIVE reads MONGO collection and writes into HIVE table

from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext, SparkSession, HiveContext
from pyspark.sql.functions import col,explode                                                                                                         
                                                                                                                                                                        
conf = SparkConf().set("spark.jars.packages","org.mongodb.spark:mongo-spark-connector_2.11:2.3.2")
                                                                                                                                                                        
                                                                                                                                                                        
spark = SparkSession.builder \
        .appName("covid19") \
        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/bigdatadb.covid19") \
        .config("spark.mongodb.output.uri","mongodb://127.0.0.1/bigdatadb.covid19") \
        .config("spark.sql.warehouse.dir", "/root/spark-warehouse") \
        .enableHiveSupport() \
        .getOrCreate()                                           
                                                                                                                                                                        
sqlContext = SQLContext(spark.sparkContext)                                                                                                                       
                                                                                                                                                                        
df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://localhost/bigdatadb.covid19").load()
                                                                                                                                                                        
df.printSchema()                                                                                                                                                       
                                                                                                                                                                        
                                                                                                                                                                        
#Database on Hive                                                                                                                                                       
spark.sql("create database bigdatadb")                                                                                                                             
                                                                                                                                                                        
                                                                                                                                                                        
df.write.mode("overwrite").saveAsTable("bigdatadb.covid19")                                                                                                            
```

#### Data Visualization
Data Visualization is achieved using Apache Zeppelin at http://127.0.0.1/9995.

### Contact
For any queries contact at:
- adharshala@trentu.ca
- Project Link: https://github.com/AdharshAla/covid19_bigdata_project.git

### Acknowledgements
- [Mongo Setup](https://github.com/nikunjness/mongo-ambari)
- [Apache Kafka Quick Start](http://www.hadoopadmin.co.in/hadoop-developer/kafka/kafka-quickstart/)
- [Apache Zeppelin Spark Interpreter](https://zeppelin.apache.org/docs/latest/interpreter/spark.html)
- [Data Visualization using Python](https://zeppelin.apache.org/docs/latest/interpreter/python.html)
