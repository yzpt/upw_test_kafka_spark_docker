git clone https://github.com/supergloo/kafka-examples.git

# 1. authentification
https://supergloo.com/kafka-tutorials/kafka-authentication/

cp kafka-examples/authentication/* .

docker compose -f kafka-authn-example.yml up -d
docker exec -it upw_test_docker_kafka_spark_nosql-kafka-1 /bin/bash

kafka-topics.sh --create --topic test-topic-auth  --bootstrap-server localhost:9092 --command-config etc/kafka/client.properties
kafka-topics.sh --list test-topic-auth  --bootstrap-server localhost:9092 --command-config etc/kafka/client.properties
# ok !

git add . && git commit -m "authentification ok"
git push --set-upstream origin zookeeper_acl


