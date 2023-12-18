import os
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "localhost:9092"

TOPIC_NAME="test-topic-auth"
SASL_USERNAME="madhu"
SASL_PASSWORD="madhu-secret"

def consume():
    consumer = KafkaConsumer(
                TOPIC_NAME, 
                security_protocol="SASL_PLAINTEXT",
                sasl_mechanism="PLAIN",
                sasl_plain_username=SASL_USERNAME,
                sasl_plain_password=SASL_PASSWORD,
                bootstrap_servers=BOOTSTRAP_SERVERS
                )
    for msg in consumer:
        print(msg)

if __name__ == "__main__":
    consume()