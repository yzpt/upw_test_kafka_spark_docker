chmod -R 777 ../pyspark_scripts/checkpoint
echo "checkpoint folder permission changed"

bin/spark-class org.apache.spark.deploy.master.Master