import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from google.cloud import bigquery
import configparser
import signal
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Configuration
temporaryGcsBucket = config.get('GCS', 'temporaryGcsBucket')
bootstrap_servers = config.get('Kafka', 'bootstrap_servers')
topic = config.get('Kafka', 'topic')
checkpointLocation = config.get('GCS', 'checkpointLocation')
key_file_path = config.get("key_file_path", "value")
spark_bigquery_jar = config.get("spark_bigquery_jar", "value")
gcs_connector_jar = config.get("gcs_connector_jar", "value")
classpath = f"{spark_bigquery_jar},{gcs_connector_jar}"

# Initialize SparkSession
spark = SparkSession.builder \
    .appName('StructuredStream') \
    .config("spark.sql.adaptive.enabled", "false")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2") \
    .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")\
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", key_file_path) \
    .config("spark.jars",classpath) \
    .getOrCreate()

# Define schema for JSON data
schema = StructType([
    StructField("message", ArrayType(StructType([
        StructField("id", StringType()),
        StructField("rank", StringType()),
        StructField("symbol", StringType()),
        StructField("name", StringType()),
        StructField("supply", StringType()),
        StructField("maxSupply", StringType()),
        StructField("marketCapUsd", StringType()),
        StructField("volumeUsd24Hr", StringType()),
        StructField("priceUsd", StringType()),
        StructField("changePercent24Hr", StringType()),
        StructField("vwap24Hr", StringType()),
        StructField("explorer", StringType()),
        StructField("timestamp", StringType())
    ])))
])

def process_batch(df, batch_id):
    json_df = df.withColumn("value", from_json("message", schema))
    exploded_df = json_df.select(explode("value.message").alias("value"))
    final_df = exploded_df.select(
        col("value.id").alias("id"),
        col("value.rank").alias("rank"),
        col("value.symbol").alias("symbol"),
        col("value.name").alias("name"),
        col("value.supply").alias("supply"),
        col("value.maxSupply").alias("maxSupply"),
        col("value.marketCapUsd").alias("marketCapUsd"),
        col("value.volumeUsd24Hr").alias("volumeUsd24Hr"),
        col("value.priceUsd").alias("priceUsd"),
        col("value.changePercent24Hr").alias("changePercent24Hr"),
        col("value.vwap24Hr").alias("vwap24Hr"),
        col("value.explorer").alias("explorer"),
        col("value.timestamp").alias("timestamp")
        )
    
    project_id = config.get('bigquery', 'project_id')
    dataset_id = config.get('bigquery', 'dataset_id')
    table_id = config.get('bigquery', 'table_id')

    try:
        final_df.write \
            .format("bigquery") \
            .mode("append") \
            .option("table", f"{project_id}.{dataset_id}.{table_id}") \
            .option("temporaryGcsBucket", temporaryGcsBucket) \
            .save()
        logger.info("Data written to BigQuery successfully")
    except Exception as e:
        logger.error(f"Failed to write data to BigQuery: {e}")
        
def stop(signal, frame):
    logger.info("Stopping the streaming query gracefully...")
    query.stop()
    logger.info("Streaming query stopped.")
    sys.exit(0)
        
def main():
    global query

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("subscribe", topic) \
        .option("failOnDataLoss", "false") \
        .option("startingOffsets", "latest") \
        .option("kafka.request.timeout.ms", "1200000") \
        .option("header", "true") \
        .load() \
        .selectExpr("CAST(value AS STRING) as message")

    query = df.writeStream \
        .format("bigquery") \
        .foreachBatch(process_batch) \
        .outputMode("append") \
        .option("checkpointLocation", checkpointLocation) \
        .start()
        
    # Register the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    
    logger.info("Streaming query started. Press Ctrl+C to stop.")
    
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected.")

if __name__ == "__main__":
    main()