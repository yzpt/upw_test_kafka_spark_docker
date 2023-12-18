import sys
import os
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"

# TOPIC_NAME="allo-topic"

SASL_USERNAME="alice"
SASL_PASSWORD="alice-secret"


def produce(topic, message):
    producer = KafkaProducer(
        security_protocol="SASL_PLAINTEXT",  
        sasl_mechanism="PLAIN", 
        sasl_plain_username=SASL_USERNAME, 
        sasl_plain_password=SASL_PASSWORD, 
        bootstrap_servers=BOOTSTRAP_SERVERS
        )
    
    producer.send(topic, message.encode())
    producer.flush()
    print('Message published successfully')

if __name__ == "__main__":
    try:
        topic = sys.argv[1]
        message = sys.argv[2]
        produce(topic, message)
    except Exception as e:
        print(f"Couldn't publish the message due to exception: {e}")
        print('use: python python1_producer.py <topic> <message>')
        sys.exit(1)