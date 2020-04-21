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

    

    