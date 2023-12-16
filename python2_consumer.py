from kafka import KafkaConsumer

if __name__ == "__main__":
    try:
        consumer = KafkaConsumer('test-topic', bootstrap_servers=['kafka:9092'])
        for message in consumer:
            print(message)
    except Exception as e:
        print('error:', e)