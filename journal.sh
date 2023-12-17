git clone https://github.com/supergloo/kafka-examples.git

# === 1. Authentification ============================================================================
https://supergloo.com/kafka-tutorials/kafka-authentication/

cp kafka-examples/authentication/* .

docker compose -f kafka-authn-example.yml up -d
docker exec -it upw_test_docker_kafka_spark_nosql-kafka-1 /bin/bash

kafka-topics.sh --create --topic test-topic-auth  --bootstrap-server localhost:9092 --command-config etc/kafka/client.properties
kafka-topics.sh --list test-topic-auth  --bootstrap-server localhost:9092 --command-config etc/kafka/client.properties
# ok !

git add . && git commit -m "authorization ongoing"
git push --set-upstream origin zookeeper_acl


# 2. === Authorization ================================================================================
https://supergloo.com/kafka-tutorials/kafka-acl/

cp kafka-examples/authorization/* .


docker compose -f kafka-authorization-example.yml up -d

docker exec -it upw_test_docker_kafka_spark_nosql-kafka-1 /bin/bash
kafka-topics.sh --create --topic test-topic-auth --bootstrap-server localhost:9092 --command-config /etc/kafka/alice-client.properties
# error : JMX 1099 binded, comment the 'JMX_PORT: 1099' line in docker-compose.yml then ok
kafka-topics.sh --list --bootstrap-server localhost:9092 --command-config /etc/kafka/alice-client.properties
kafka-topics.sh --list --bootstrap-server localhost:9092 # to check if authentification is working (waiting timeout)

# Let’s have Madhu and Alice both produce some gibberish to the test-topic-auth topic to show they can both publish to it.

kafka-console-producer.sh --topic test-topic-auth --broker-list localhost:9092 --producer.config /etc/kafka/alice-client.properties
kafka-console-producer.sh --topic test-topic-auth --broker-list localhost:9092 --producer.config /etc/kafka/madhu-client.properties

# And now, prove they can both consume from it.
kafka-console-consumer.sh --topic test-topic-auth --bootstrap-server localhost:9092 --consumer.config /etc/kafka/alice-client.properties --from-beginning
kafka-console-consumer.sh --topic test-topic-auth --bootstrap-server localhost:9092 --consumer.config /etc/kafka/madhu-client.properties --from-beginning



