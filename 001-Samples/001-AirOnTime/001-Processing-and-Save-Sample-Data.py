# Databricks notebook source
df = spark.read.format("csv").option("inferSchema", "true").option("header","true").load("dbfs:/mnt/rawdata/001-AirOnTime/*.csv")

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE AirOnTimeDB.AirOnTime

# COMMAND ----------

df.write.format("delta").partitionBy("YEAR").mode("overwrite").saveAsTable("AirOnTimeDB.AirOnTime")
# NOT NEED BELOW SCRIPT
# df.write.format("delta").partitionBy("YEAR").mode("overwrite").save(SaveFolderAirOnTime)