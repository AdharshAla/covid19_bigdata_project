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