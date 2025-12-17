# 1️⃣ Kafka + Docker (⏱ 1–2 hrs) (Completed 🍾)
### Goal

Bring up **all infra in one command**.

---

## What to Run (Minimum Services)

| Service       | Why                    |
| ------------- | ---------------------- |
| Zookeeper     | Kafka dependency       |
| Kafka         | Streaming backbone     |
| MongoDB       | Raw + enriched storage |
| Elasticsearch | Analytics backend      |
| Kibana        | Visualization          |

---

## Steps

### Step 1: Docker Compose Skeleton

Create `docker-compose.yml`

Services:

-   `zookeeper`
-   `kafka`
-   `mongo`
-   `elasticsearch`
-   `kibana`

---

### Step 2: Kafka Config (Important for Local)

Key configs:

```yaml
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
```

👉 Avoid networking issues
👉 Single broker = fastest

---

### Step 3: Verify Services

Run:

```bash
docker compose up -d
```

Check:

-   Kafka running
-   Mongo at `localhost:27017`
-   Kibana at `http://localhost:5601`

---

### Output of This Stage

✅ Kafka broker
✅ Mongo DB
✅ Elasticsearch
✅ Kibana UI

---

# 2️⃣ Kafka Producer (⏱ 30 mins)

### Goal

Simulate **streaming Yelp reviews**.

---

## Input

-   `yelp_academic_dataset_review.json`
-   JSON Lines format

---

## Producer Flow

```text
Read file → parse JSON → sleep → send to Kafka
```

---

## Key Decisions

| Choice       | Reason         |
| ------------ | -------------- |
| Python       | Fast to write  |
| kafka-python | Lightweight    |
| 1 topic      | MVP simplicity |

---

## Core Logic

-   Read one review at a time
-   Send to `raw_reviews`
-   `time.sleep(random.uniform(0.1, 0.3))`

---

## Validation

Run producer and check:

```bash
kafka-console-consumer --topic raw_reviews
```

---

## Output of This Stage

✅ Streaming data visible in Kafka
✅ Controlled throughput

---

# 3️⃣ Kafka Consumer + MongoDB (⏱ 1 hr)

### Goal

Persist raw data reliably.

---

## Consumer Flow

```text
Kafka → Consumer → MongoDB
```

---

## Consumer Responsibilities

-   Deserialize JSON
-   Add `ingest_time`
-   Insert into Mongo

---

## Mongo Collections

### `raw_reviews`

```json
{
  review_id,
  text,
  stars,
  ingest_time
}
```

---

## Key Config

```python
auto_offset_reset="earliest"
enable_auto_commit=True
```

---

## Validation

```bash
db.raw_reviews.countDocuments()
```

---

## Output of This Stage

✅ Kafka → Mongo pipeline working
✅ Raw data safely stored

---

# 4️⃣ Sentiment Models (⏱ 1.5 hrs)

### Goal

Compare **simple model vs BERT**

---

## Model A: Baseline (Your Model)

### Choice

**VADER** or **TextBlob**

Why?

-   No training
-   Instant output
-   Interpretable

---

### Output

```json
{
  sentiment_score,
  sentiment_label
}
```

---

## Model B: BERT (Pretrained)

### Model

```text
distilbert-base-uncased-finetuned-sst-2-english
```

---

### Output

```json
{
  bert_label,
  bert_confidence
}
```

---

## Enrichment Flow

```text
raw_reviews → sentiment inference → enriched_reviews
```

---

## Mongo: `enriched_reviews`

```json
{
  review_id,
  stars,
  baseline_sentiment,
  bert_sentiment,
  timestamp
}
```

---

## Output of This Stage

✅ Two sentiment outputs
✅ Structured comparison data

---

# 5️⃣ Elasticsearch + Kibana (⏱ 1–2 hrs)

### Goal

Enable analytics & visualization.

---

## Elasticsearch Index

Create index:

```text
yelp_sentiment
```

---

## Index Mapping (Simple)

```json
stars: integer
baseline_label: keyword
bert_label: keyword
timestamp: date
```

---

## Data Push Strategy

Python script:

-   Read from Mongo
-   Bulk insert into ES

Why?

-   Faster than real-time for MVP
-   Easier debugging

---

## Kibana Setup

-   Create Index Pattern
-   Select timestamp field

---

## Output of This Stage

✅ Searchable sentiment data
✅ Kibana ready

---

# 6️⃣ Dashboard (⏱ 1 hr)

### Goal

Show **value, not complexity**

---

## Dashboard Components

### 1️⃣ Sentiment Distribution

-   Pie chart
-   Compare baseline vs BERT

---

### 2️⃣ Sentiment vs Stars

-   Bar chart
-   Avg sentiment per rating

---

### 3️⃣ Sentiment Over Time

-   Line chart
-   Volume trends

---

### 4️⃣ Model Agreement

-   Table
-   baseline_label vs bert_label

---

## Why This Works

-   Business readable
-   ML visible
-   Streaming story complete

---

## Output of This Stage

✅ Executable story
✅ Recruiter-friendly visuals

---

# 🧠 Final MVP Story (What You Say)

> “I built a real-time sentiment analysis pipeline using Kafka. Yelp reviews are streamed, stored raw in MongoDB, enriched using both a rule-based and BERT model, indexed into Elasticsearch, and visualized in Kibana for trend and model comparison.”

---

## Want Next?

I can now:
1️⃣ Give **docker-compose.yml**
2️⃣ Write **producer + consumer code**
3️⃣ Provide **sentiment inference script**
4️⃣ Give **Kibana dashboard screenshots + JSON**
5️⃣ Help convert this into **resume bullets**

Just say the number 👌
