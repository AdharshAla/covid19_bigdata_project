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