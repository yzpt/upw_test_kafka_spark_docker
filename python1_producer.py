from kafka import KafkaProducer
import sys

if __name__ == "__main__":
    try:
        # producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="PLAIN",
            sasl_plain_username="admin",
            sasl_plain_password="admin-secret",
        )
    
        message = sys.argv[1]
        
        producer.send(topic='test-topic', value=message.encode())
        producer.flush()

        print("Message sent successfully")

    except Exception as e:
        print('error:', e)
