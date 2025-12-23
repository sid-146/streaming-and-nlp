from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf, current_timestamp
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    FloatType,
    IntegerType,
)
from transformers import pipeline

from src.common.config_loader import load_config


import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

sentiment_pipeline = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


def analyze_sentiment(text):
    if text and isinstance(text, str):
        try:
            result = sentiment_pipeline(text)[0]
            return result["label"]
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return "Error"
    return "Empty or Invalid"


def run():
    spark = (
        SparkSession.builder.appName("yelp_review_consumer")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
        )
        .getOrCreate()
    )

    spark.conf.set(
        "spark.sql.streaming.checkpointLocation",
        "/opt/spark-data/yelp_review_consumer/checkpoints",
    )

    logger.info("created spark session")

    kafka_config = load_config("kafka.yaml")["kafka"]["consumers"][
        "yelp_review_consumer"
    ]
    mongo_config = load_config("mongo.yaml")["enriched_review"]

    logger.info("Configs Extracted.")

    schema = StructType(
        [
            StructField("review_id", StringType()),
            StructField("user_id", StringType()),
            StructField("business_id", StringType()),
            StructField("stars", FloatType()),
            StructField("useful", IntegerType()),
            StructField("funny", IntegerType()),
            StructField("cool", IntegerType()),
            StructField("text", StringType()),
            StructField("date", StringType()),
        ]
    )

    stream_df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", ",".join(kafka_config["bootstrap_servers"]))
        .option("subscribe", kafka_config["topic"])
        .option("startingOffsets", "earliest")
        .load()
    )
    parsed_df = stream_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    logger.info("Streaming DF created.")

    sentiment_udf = udf(analyze_sentiment, StringType())
    enriched_df = parsed_df.withColumn(
        "sentiment", sentiment_udf(col("text"))
    ).withColumn("timestamp", current_timestamp())

    logger.info("Enriched DF created.")

    # # Format: mongodb://[username:password@]host[:port]/[database.collection]
    mongo_uri = f"mongodb://{mongo_config['username']}:{mongo_config['password']}@{mongo_config['host']}:{mongo_config['port']}"
    (
        enriched_df.writeStream.format("mongodb")
        .option("spark.mongodb.connection.uri", mongo_uri)
        .option("spark.mongodb.database", mongo_config["database"])
        .option("spark.mongodb.collection", mongo_config["collection"])
        # .option("checkpointLocation", checkpoint_dir)
        .outputMode("append")
        .start()
        .awaitTermination()
    )

    logger.info("Terminating Process.")


if __name__ == "__main__":
    run()
