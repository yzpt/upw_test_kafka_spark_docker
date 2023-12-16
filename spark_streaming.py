
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, when
from pyspark.sql.types import StructType,StructField,FloatType,StringType, LongType
from pyspark.sql.functions import current_timestamp

import uuid

def create_spark_session():
    """
    Creates the Spark Session with suitable configs.
    """
    try:
        # Spark session is established with kafka jars. Suitable versions can be found in Maven repository.
        spark = SparkSession \
                .builder \
                .appName("SparkStructuredStreaming") \
                .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
                .config("spark.cassandra.connection.host", "cassandra") \
                .config("spark.cassandra.connection.port","9042")\
                .config("spark.cassandra.auth.username", "cassandra") \
                .config("spark.cassandra.auth.password", "cassandra") \
                .getOrCreate()
        # Get the SparkConf from the Spark session
        conf = spark._jsc.getConf()
        # Set the value for spark.maxRemoteBlockSizeFetchToMem
        conf.set("spark.maxRemoteBlockSizeFetchToMem", "1g")  # to avoid the 'too large frame' error when blocksize >= 2g

        spark.sparkContext.setLogLevel("ERROR")
        print('Spark session created successfully')
    except Exception:
        print("Couldn't create the spark session")

    return spark


def create_initial_dataframe(spark_session):
    """
    Reads the streaming data and creates the initial dataframe accordingly.
    """
    try:
        # Gets the streaming data from topic random_names
        df = spark_session \
              .readStream \
              .format("kafka") \
              .option("kafka.bootstrap.servers", "kafka:9092") \
              .option("subscribe", "test-topic") \
              .option("delimeter",",") \
              .option("startingOffsets", "earliest") \
              .option("failOnDataLoss", "false") \
              .load()

        print("Initial dataframe created successfully")
    except Exception as e:
        print(f"Initial dataframe couldn't be created due to exception: {e}")

    return df



def create_final_dataframe(df, spark_session):
    """
    Modifies the initial dataframe, and creates the final dataframe.
    """

    df = df.selectExpr("CAST(value AS STRING)", "CAST(timestamp AS STRING)")
    uuidUdf= udf(lambda : str(uuid.uuid4()),StringType())
    df = df.withColumn("id", uuidUdf())

    # Add "dest_table" column
    df = df.withColumn("destination_table", when(col("value").contains("help"), "help").otherwise("messages"))

    return df


def start_console_streaming(df):
    """
    Starts the streaming to console
    """
    my_query = (df.writeStream
                  .format("console")
                  .outputMode("append")
                  .start())

    return my_query.awaitTermination()

def print_to_console(df, epoch_id):
    df.show()

# def start_cassandra_streaming(df):
#     """
#     Starts the streaming to table spark_streaming.random_names in cassandra
#     """

#     destination_table = df.select("destination_table").collect()[0][0]
#     print('dest_talbe:', destination_table)

#     my_query = (df.writeStream
#                   .format("org.apache.spark.sql.cassandra")
#                   .outputMode("append")
#                   .option("checkpointLocation", "checkpoint")
#                   .options(table=destination_table, keyspace="spark_streaming")
#                   .start())
#                 #   .foreachBatch(print_to_console)

#     return my_query.awaitTermination()

def start_cassandra_streaming(df):
    """
    Starts the streaming to table spark_streaming.random_names in cassandra
    """

    def write_to_cassandra(df, epoch_id):
        destination_table = df.select("destination_table").first()[0]
        (df.write
            .format("org.apache.spark.sql.cassandra")
            .options(table=destination_table, keyspace="spark_streaming")
            .mode("append")
            .save())

    my_query = (df.writeStream
                  .foreachBatch(write_to_cassandra)
                  .outputMode("append")
                  .option("checkpointLocation", "checkpoint")
                  .start())

    return my_query.awaitTermination()



def write_streaming_data():
    spark       = create_spark_session()
    df          = create_initial_dataframe(spark)
    df_final    = create_final_dataframe(df, spark)

    
    # start_console_streaming(df)
    
    # df_final = create_final_dataframe(df, spark)
    start_cassandra_streaming(df_final)

if __name__ == '__main__':
    try:
        write_streaming_data()
    except Exception as e:
        print('error')
        print(e)
