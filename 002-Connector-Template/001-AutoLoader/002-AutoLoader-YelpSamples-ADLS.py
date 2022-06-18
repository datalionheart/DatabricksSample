# Databricks notebook source
spark.conf.set("spark.databricks.delta.properties.defaults.autoOptimize.optimizeWrite", "true")
spark.conf.set("spark.databricks.delta.properties.defaults.autoOptimize.autoCompact", "true")

# COMMAND ----------

spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/databases/yelp_academic_dataset/raw_user") \
  .option("cloudFiles.inferColumnTypes", "true") \
  .load("dbfs:/mnt/stagedata/002-Yelp-Datasets/*yelp_academic_dataset_user.json") \
  .writeStream \
  .format("delta") \
  .queryName("AutoLoader-From-ADLS-ETL-Yelp-User") \
  .outputMode("append") \
  .option("checkpointLocation", "dbfs:/mnt/databases/yelp_academic_dataset/raw_user/_checkpoints/etl-from-json") \
  .start("dbfs:/mnt/databases/yelp_academic_dataset/raw_user")

# COMMAND ----------

from pyspark.sql.functions import explode, split
df = df.withColumn("friends", explode(split(df["friends"], ", "))) \
       .withColumn("elite", explode(split(df["elite"], ",")))

# COMMAND ----------

# MAGIC %sh
# MAGIC ls /dbfs//mnt/stagedata/002-Yelp-Datasets/

# COMMAND ----------

spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/databases/yelp_academic_dataset/raw_tip") \
  .option("cloudFiles.inferColumnTypes", "true") \
  .load("dbfs:/mnt/stagedata/002-Yelp-Datasets/*yelp_academic_dataset_tip.json") \
  .writeStream \
  .format("delta") \
  .queryName("AutoLoader-From-ADLS-ETL-Yelp-User") \
  .outputMode("append") \
  .option("checkpointLocation", "dbfs:/mnt/databases/yelp_academic_dataset/raw_tip/_checkpoints/etl-from-json") \
  .start("dbfs:/mnt/databases/yelp_academic_dataset/raw_tip")

# COMMAND ----------

spark.readStream.format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "dbfs:/mnt/databases/yelp_academic_dataset/raw_business") \
  .option("cloudFiles.inferColumnTypes", "true") \
  .load("dbfs:/mnt/stagedata/002-Yelp-Datasets/*yelp_academic_dataset_business.json") \
  .writeStream \
  .format("delta") \
  .queryName("AutoLoader-From-ADLS-ETL-Yelp-User") \
  .outputMode("append") \
  .option("checkpointLocation", "dbfs:/mnt/databases/yelp_academic_dataset/raw_business/_checkpoints/etl-from-json") \
  .start("dbfs:/mnt/databases/yelp_academic_dataset/raw_business")