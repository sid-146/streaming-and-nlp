import subprocess

SPARK_SUBMIT_CMD = [
    "docker",
    "exec",
    "-i",
    "spark-stream-master",
    "spark-submit",
    "--master",
    "spark://spark-stream-master:3033",
    "--conf",
    "spark.driver.host=spark-stream-master",
    "--conf",
    "spark.driver.bindAddress=0.0.0.0",
    "--packages",
    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7,"
    "org.apache.kafka:kafka-clients:3.6.1,"
    "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0",
    "--py-files",
    "/opt/spark-apps/src",
    "/opt/spark-apps/yelp_review_consumer.py",
]


def trigger_streaming():
    print("Starting Spark Streaming Job...")
    subprocess.run(SPARK_SUBMIT_CMD, check=True)


if __name__ == "__main__":
    trigger_streaming()
