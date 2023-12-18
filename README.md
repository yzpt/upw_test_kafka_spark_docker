# Kafka Authorization by Example

[https://supergloo.com/kafka-tutorials/kafka-acl-authorization](https://supergloo.com/kafka-tutorials/kafka-acl-authorization/)

# work --> [journal.sh](journal.sh)

```bash
git clone https://github.com/supergloo/kafka-examples.git

# === 1. Authentification ============================================================================
https://supergloo.com/kafka-tutorials/kafka-authentication/

cp kafka-examples/authentication/* .

docker compose -f kafka-authn-example.yml up -d
docker exec -it upw_test_docker_kafka_spark_nosql-kafka-1 /bin/bash
docker exec -it kafka /bin/bash

kafka-topics.sh --create --topic test-topic  --bootstrap-server localhost:9092 --command-config etc/kafka/client.properties
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

# apply first ACLs
kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:alice --operation Read --allow-host '*' --topic test-topic-auth --command-config /etc/kafka/admin-client.properties

# And now the following attempt which succeeded before, will now fail.
kafka-console-producer.sh --topic test-topic-auth --broker-list localhost:9092 --producer.config /etc/kafka/alice-client.properties

# Let’s continue with our desired outcome and set ACLs for Madhu to be able to both produce and consumer from the Kafka topic.
kafka-acls.sh --bootstrap-server localhost:9092 --add --allow-principal User:madhu --operation Read --operation Write --allow-host '*' --topic test-topic-auth --command-config /etc/kafka/admin-client.properties
# Notice how we are passing in two operation variable values in the above command.

# Let’s confirm Madhu can still produce to the topic.
kafka-console-producer.sh --topic test-topic-auth --broker-list localhost:9092 --producer.config /etc/kafka/madhu-client.properties

# madhu consumer
kafka-console-consumer.sh --topic test-topic-auth --bootstrap-server localhost:9092 --consumer.config /etc/kafka/madhu-client.properties --from-beginning

docker exec -it upw_test_docker_kafka_spark_nosql-kafka-1 /bin/bash
kafka-console-consumer.sh --topic test-topic-auth --bootstrap-server localhost:9092 --consumer.config /etc/kafka/madhu-client.properties --from-beginning



# === python producer & consumer =====================================================================
https://gist.github.com/alexlopes/72fea4e4da623ef8f60a800d6a962f2f
# -> python1_producer.py
# -> python2_consumer.py

# python producer & consumer with sasl plaintext auth ok, authorization ok, see also py_admin_acl.py for administration.

git add . && git commit -m "python client & Kafka ACL ok, spark streaming doesn't work"
git push --set-upstream origin zookeeper_acl

git checkout -b zookeeper_acl_backup
git checkout zookeeper_acl

# === project implementation =========================================================================
# -> docker-compose.yml
docker compose up -d
docker exec -it kafka /bin/bash

# create topic with admin-client.properties
kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --command-config /etc/kafka/admin-client.properties

# set ACLs with admin-client.properties, allow alice to read and write
kafka-acls.sh \
    --bootstrap-server localhost:9092 \
    --add \
    --allow-principal User:alice \
    --operation Read \
    --operation Write \
    --allow-host '*' \
    --topic test-topic \
    --command-config /etc/kafka/admin-client.properties

# set ACLs with admin-client.properties, allow madhu to read only
kafka-acls.sh \
    --bootstrap-server localhost:9092 \
    --add \
    --allow-principal User:madhu \
    --operation Read \
    --allow-host '*' \
    --topic test-topic \
    --command-config /etc/kafka/admin-client.properties

# admin consumer
kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --consumer.config /etc/kafka/admin-client.properties --from-beginning

# alice consumer
kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --consumer.config /etc/kafka/alice-client.properties --from-beginning

# python producer
python3 python1_producer.py "message"

# ok !
cp ~/Downloads/spark_streaming.py .
docker compose up -d

#  === Cassandra ========================================================================
docker exec -it cassandra /bin/bash
cqlsh -u cassandra -p cassandra
CREATE KEYSPACE spark_streaming WITH replication = {'class':'SimpleStrategy','replication_factor':1};

DROP TABLE spark_streaming.help;
DROP TABLE spark_streaming.messages;

# create help table
CREATE TABLE spark_streaming.help(
    id uuid PRIMARY KEY,
    content text,
    value text,
    timestamp text,
    destination_table text
);

# create messages table
CREATE TABLE spark_streaming.messages(
    id uuid PRIMARY KEY,
    content text,
    value text,
    timestamp text,
    destination_table text
);

select value, destination_table from spark_streaming.help;
select value, destination_table from spark_streaming.messages;

truncate spark_streaming.help;
truncate spark_streaming.messages;


# === Spark =================================================================================
docker compose down spark-master spark-worker
docker compose up -d spark-master spark-worker

# https://stackoverflow.com/questions/61481628/spark-structured-streaming-with-kafka-sasl-plain-authentication
docker exec -it spark-master /bin/bash -c "spark-submit --master local --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 /opt/bitnami/pyspark_scripts/spark_streaming.py"

# doesn't seems to connect to kafka
# -> https://stackoverflow.com/questions/61481628/spark-structured-streaming-with-kafka-sasl-plain-authentication
# -> spark_streaming.py
```