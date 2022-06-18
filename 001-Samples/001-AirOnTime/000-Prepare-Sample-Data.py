# Databricks notebook source
# MAGIC %sh
# MAGIC wget https://packages.revolutionanalytics.com/datasets/AirOnTime87to12/AirOnTimeCSV.zip --no-check-certificate

# COMMAND ----------

# MAGIC %sh
# MAGIC zip -FF AirOnTimeCSV.zip --out AirOnTimeCSV_fixed.zip

# COMMAND ----------

# MAGIC %sh
# MAGIC unzip ./AirOnTimeCSV_fixed.zip

# COMMAND ----------

# MAGIC %sh
# MAGIC pwd

# COMMAND ----------

dbutils.fs.mv("file:/databricks/driver/AirOnTimeCSV/", "dbfs:/mnt/rawdata/001-AirOnTime/", recurse=True)

# COMMAND ----------

df = spark.read.format("csv") \
    .option("inferSchema", "true") \
    .option("header","true") \
    .load("dbfs:/mnt/rawdata/001-AirOnTime/*.csv")

# COMMAND ----------

display(df)

# COMMAND ----------

spark.catalog.clearCache()

# COMMAND ----------

dbutils.fs.ls('dbfs:/mnt/rawdata/001-AirOnTime/')