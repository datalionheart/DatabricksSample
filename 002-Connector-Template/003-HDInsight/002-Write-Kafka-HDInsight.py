# Databricks notebook source
# MAGIC %md
# MAGIC # Deploy HDInsight Kafka Cluster
# MAGIC Example show as below snapshot:
# MAGIC ![](https://databricksdocs.blob.core.chinacloudapi.cn/images/HDIKafka002.png)
# MAGIC ![](https://databricksdocs.blob.core.chinacloudapi.cn/images/HDIKafka003.png)
# MAGIC ![](https://databricksdocs.blob.core.chinacloudapi.cn/images/HDIKafka001.png)

# COMMAND ----------

# MAGIC %md
# MAGIC # Manage Kafka Topic
# MAGIC ```bash
# MAGIC export KAFKAZKHOSTS=192.168.6.10,192.168.6.12,192.168.6.13
# MAGIC /usr/hdp/current/kafka-broker/bin/kafka-topics.sh --list --zookeeper $KAFKAZKHOSTS
# MAGIC /usr/hdp/current/kafka-broker/bin/kafka-topics.sh --create --replication-factor 3 --partitions 3 --topic test --zookeeper $KAFKAZKHOSTS
# MAGIC /usr/hdp/current/kafka-broker/bin/kafka-topics.sh --delete --topic test --zookeeper $KAFKAZKHOSTS
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./001-AutoLoader/000-Schema-AirOnTime

# COMMAND ----------

df = spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .option("header", "true") \
        .schema(customSchema) \
        .load("dbfs:/mnt/rawdata/001-AirOnTime/*.csv")

# COMMAND ----------

from pyspark.sql.functions import *

df.select(to_json(struct("*")).alias("value")) \
  .selectExpr("CAST(value AS STRING)") \
  .writeStream \
  .queryName("AutoLoader-From-ADLS-ETL-AirOnTime-2-Kafka") \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "192.168.6.4:9092,192.168.6.5:9092,192.168.6.6:9092") \
  .option("topic", "databricks") \
  .option("checkpointLocation", "dbfs:/mnt/rawdata/kafka/topic_databricks/_checkpoint/") \
  .start()

# COMMAND ----------

dfsql = spark.readStream.format("delta").schema(customSchema).table("airontimedb.airontime")

# COMMAND ----------

from pyspark.sql.functions import *

dfsql.select(to_json(struct("*")).alias("value")) \
  .selectExpr("CAST(value AS STRING)") \
  .writeStream \
  .queryName("AutoLoader-From-ADLS-ETL-AirOnTime-2-Kafka") \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "192.168.6.4:9092,192.168.6.5:9092,192.168.6.6:9092") \
  .option("topic", "airontime") \
  .option("checkpointLocation", "dbfs:/mnt/rawdata/kafka/topic_airontime/_checkpoint/") \
  .start()