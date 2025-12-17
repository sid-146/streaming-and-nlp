import socket
import requests
from confluent_kafka.admin import AdminClient
from pymongo import MongoClient


# ---------------- CONFIG ----------------
ZOOKEEPER_HOST = "localhost"
ZOOKEEPER_PORT = 2181

KAFKA_BOOTSTRAP = "localhost:29092"
KAFKA_UI_URL = "http://localhost:8080"

MONGO_URI = "mongodb://admin:password@localhost:27017/"
ELASTIC_URL = "http://localhost:9200"
KIBANA_URL = "http://localhost:5601"


# ---------------- HELPERS ----------------
def ok(msg):
    print(f"✅ {msg}")


def fail(msg, err):
    print(f"❌ {msg} → {err}")


# ---------------- CHECKS ----------------
def check_zookeeper():
    try:
        with socket.create_connection(
            (ZOOKEEPER_HOST, ZOOKEEPER_PORT), timeout=5
        ) as sock:
            sock.sendall(b"ruok\n")
            resp = sock.recv(1024).decode().strip()
            if resp == "imok":
                ok("Zookeeper is healthy")
            else:
                fail("Zookeeper unhealthy response", resp)
    except Exception as e:
        fail("Zookeeper not reachable", e)


def check_kafka():
    try:
        admin = AdminClient({"bootstrap.servers": "localhost:29092"})
        topics = admin.list_topics(timeout=5).topics
        print(f"✅ Kafka is healthy (topics: {len(topics)})")
    except Exception as e:
        print(f"❌ Kafka not reachable → {e}")


def check_kafka_ui():
    try:
        r = requests.get(KAFKA_UI_URL, timeout=5)
        if r.status_code == 200:
            ok("Kafka UI is reachable")
        else:
            fail("Kafka UI bad response", r.status_code)
    except Exception as e:
        fail("Kafka UI not reachable", e)


def check_mongodb():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        ok("MongoDB is healthy")
        client.close()
    except Exception as e:
        fail("MongoDB not reachable", e)


def check_elasticsearch():
    try:
        r = requests.get(f"{ELASTIC_URL}/_cluster/health", timeout=5)
        data = r.json()
        ok(f"Elasticsearch is healthy (status: {data['status']})")
    except Exception as e:
        fail("Elasticsearch not reachable", e)


def check_kibana():
    try:
        r = requests.get(KIBANA_URL, timeout=5)
        if r.status_code == 200:
            ok("Kibana is reachable")
        else:
            fail("Kibana bad response", r.status_code)
    except Exception as e:
        fail("Kibana not reachable", e)


# ---------------- RUN ALL ----------------
if __name__ == "__main__":
    print("\n🔍 Running Streaming Stack Health Check\n")

    check_zookeeper()
    check_kafka()
    check_kafka_ui()
    check_mongodb()
    check_elasticsearch()
    check_kibana()

    print("\n✅ Health check completed\n")
