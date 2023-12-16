from kafka import KafkaProducer
import sys

if __name__ == "__main__":
    try:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
    
        message = sys.argv[1]
        
        producer.send(topic='test-topic', value=message.encode())
        producer.flush()

        print("Message sent successfully")

    except Exception as e:
        print('error:', e)