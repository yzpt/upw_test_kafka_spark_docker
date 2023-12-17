# docker
docker compose down
docker compose up -d

# venv
python3 -m venv venv
source venv/bin/activate

# pip
pip install kafka-python
pip install pyspark


# === Kafka ========================================================================
# create topic
topic=test-topic
server=kafka:9092

# create topic
docker exec kafka opt/bitnami/kafka/bin/kafka-topics.sh --create --topic $topic --bootstrap-server $server
# kafka consumer
docker exec kafka opt/bitnami/kafka/bin/kafka-console-consumer.sh --topic $topic --from-beginning --bootstrap-server $server
# kafka producer
docker exec kafka opt/bitnami/kafka/bin/kafka-console-producer.sh --topic $topic --bootstrap-server $server

# py produce message on kafka
python3 python1_producer.py "message content"

# py consume message on kafka
python3 python2_consumer.py


# === Spark ========================================================================
docker compose down  spark-master spark-worker
docker compose up -d spark-master spark-worker  

# start streaming:
docker exec -it spark-master /bin/bash -c "spark-submit --master local --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 /opt/bitnami/pyspark_scripts/spark_streaming.py"


# === Cassandra ========================================================================
# connect to cassandra container
docker exec -it cassandra /bin/bash

# connect to cassandra
cqlsh -u cassandra -p cassandra

# create keyspace
CREATE KEYSPACE spark_streaming WITH replication = {'class':'SimpleStrategy','replication_factor':1};

# drop table
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


# data insertion ok !




# === git =========================================================
git init
touch .gitignore && code .gitignore
git add .
git commit -m "first commit"
git remote add origin https://github.com/yzpt/upw_test_kafka_spark_docker.git
git push --set-upstream origin main

touch README.MD && code README.MD

git add . && git commit -m "update" && git push


# === Zookeeper mode ========================================================================
# no ACL with Kraft mode !

git checkout -b zookeeper_mode

# -> docker-compose
docker compose up -d zookeeper 
docker compose up -d zookeeper broker 
docker compose up -d zookeeper broker schema-registry 
docker compose up -d zookeeper broker schema-registry control-center

# docker create topic
docker exec broker kafka-topics --create --topic test-topic --bootstrap-server broker:9092

# python producer
python3 python1_producer.py "allo"

# deploy pipeline
docker compose up -d zookeeper broker schema-registry control-center spark-master spark-worker cassandra

# start spark streaming
docker exec -it spark-master /bin/bash -c "spark-submit --master local --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 /opt/bitnami/pyspark_scripts/spark_streaming.py"

# send a message
python3 python1_producer.py "message without h_elp word"
python3 python1_producer.py "message with help word"

# check cassandra
docker exec -it cassandra /bin/bash
cqlsh -u cassandra -p cassandra
select value, destination_table from spark_streaming.help;
select value, destination_table from spark_streaming.messages;

# no insertion in cassandra
# -> spark_streaming.py change "kafka:9092" to "broker:29092" and restart spark streaming

docker compose down spark-master spark-worker
docker compose up -d spark-master spark-worker
docker exec -it spark-master /bin/bash -c "spark-submit --master local --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.4.1 /opt/bitnami/pyspark_scripts/spark_streaming.py"

python3 python1_producer.py "without the word"
python3 python1_producer.py "with help word"

# check cassandra --> pipeline ok.
git add . && git commit -m "zookeeper mode pipeline ok"
git push --set-upstream origin zookeeper_mode

# === ACL ==============================================================================
# https://www.youtube.com/watch?v=bj5SKXanaAI

docker compose down
docker compose up -d zookeeper broker

mkdir configs
touch configs/kafka_server_jaas.conf && code configs/kafka_server_jaas.conf
# --- kafka_server_jaas.conf ---
KafkaServer {
    org.apache.kafka.common.security.plain.PlainLoginModule required
    username="admin"
    password="pass123"
    user_kafka="pass123";
}
# ------------------------------

touch configs/config.properties && code configs/config.properties
# --- config.properties ---
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="admin" password="pass123";
security.protocol=SASL_PLAINTEXT
sasl.mechanism=PLAIN
# ------------------------------

docker compose down
docker compose up -d zookeeper broker

docker exec -it broker /bin/bash
kafka-topics --create --topic allo-topic --bootstrap-server broker:9093 --replication-factor 1 --partitions 1 --command-config /etc/kafka/configs/config.properties

# === stop
git add . && git commit -m "stop, go SASL branch"