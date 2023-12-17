import os
from kafka import KafkaProducer, KafkaConsumer

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")

TOPIC_NAME="test-topic-auth"
SASL_USERNAME="madhu"
SASL_PASSWORD="madhu-secret"


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