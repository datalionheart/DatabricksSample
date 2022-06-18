# Databricks notebook source
kafka = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "192.168.2.134:9093,192.168.2.140:9093,192.168.2.141:9093")  \
  .option("subscribe", "fsmy4debezium.mysql.database.azure.com.classicmodels.demo") \
  .option("startingOffsets", "latest") \
  .load()

# COMMAND ----------

from pyspark.sql.functions import get_json_object, col
kafka = kafka.select(col("value").cast("string"), \
                     col("topic").cast("string"))

kafka = kafka.withColumn("database", get_json_object(col("value"), "$.payload.source.db")) \
            .withColumn("table", get_json_object(col("value"), "$.payload.source.table")) \
            .withColumn("op", get_json_object(col("value"), "$.payload.op")) \
            .withColumn("before", get_json_object(col("value"), "$.payload.before")) \
            .withColumn("after", get_json_object(col("value"), "$.payload.after")) \
            .withColumn("ts_ms", get_json_object(col("value"), "$.payload.source.ts_ms")) \
            .withColumn("file", get_json_object(col("value"), "$.payload.source.file")) \
            .withColumn("pos", get_json_object(col("value"), "$.payload.source.pos")) \
            .withColumn("name", get_json_object(col("value"), "$.payload.source.name")) \
            .drop("value") \
            .drop("topic")

# COMMAND ----------

display(kafka)