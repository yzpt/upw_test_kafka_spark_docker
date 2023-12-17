import sys
import os
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"

TOPIC_NAME="test-topic"

SASL_USERNAME="alice"
SASL_PASSWORD="alice-secret"


def produce():
    producer = KafkaProducer(
        security_protocol="SASL_PLAINTEXT",  
        sasl_mechanism="PLAIN", 
        sasl_plain_username=SASL_USERNAME, 
        sasl_plain_password=SASL_PASSWORD, 
        bootstrap_servers=BOOTSTRAP_SERVERS
        )
    
    producer.send(TOPIC_NAME, b'some_message_bytes')
    producer.flush()
    print('Message published successfully')

if __name__ == "__main__":
    produce()