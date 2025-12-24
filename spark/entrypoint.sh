#!/bin/bash
set -e

if [ "$SPARK_MODE" = "master" ]; then
    echo "Starting Spark Master"

    exec /opt/spark/bin/spark-class \
      org.apache.spark.deploy.master.Master \
      --host 0.0.0.0 \
      --port "$MASTER_PORT" \
      --webui-port "$WEBUI_PORT"

elif [ "$SPARK_MODE" = "worker" ]; then
    echo "Starting Spark Worker"

    exec /opt/spark/bin/spark-class \
      org.apache.spark.deploy.worker.Worker \
      "$SPARK_MASTER_URL" \
      --host 0.0.0.0 \
      --port "$WORKER_PORT" \
      --webui-port "$SPARK_WORKER_WEBUI_PORT"
else
    echo "Invalid SPARK_MODE"
    exit 1
fi
