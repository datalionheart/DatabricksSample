# Databricks notebook source
# MAGIC %md
# MAGIC * Schema on READ
# MAGIC   * Predefined schema on notebook as parameters to use to AutoLoader(option: schema)

# COMMAND ----------

spark.conf.set("spark.databricks.cloudFiles.schemaInference.sampleSize.numBytes", "256mb")
spark.conf.set("spark.databricks.cloudFiles.schemaInference.sampleSize.numFiles", "1")

# COMMAND ----------

# MAGIC %run ./000-Schema-AirOnTime

# COMMAND ----------

# MAGIC %run ./000-Table-Create-AirOnTime

# COMMAND ----------

spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "csv") \
  .option("header", "true") \
  .schema(customSchema) \
  .load("dbfs:/mnt/rawdata/001-AirOnTime/*.csv") \
  .writeStream \
  .format("delta") \
  .queryName("AutoLoader-From-ADLS-ETL-AirOnTime") \
  .outputMode("append") \
  .option("checkpointLocation", "dbfs:/mnt/databases/airontimedb/airontime_streaming_001/_checkpoints/etl-from-csv") \
  .table("airontimedb.airontime_streaming_001")