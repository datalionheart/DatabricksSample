# Databricks notebook source
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
customSchema = StructType([StructField("YEAR", IntegerType(), True),
    StructField("MONTH", IntegerType(), True),
    StructField("DAY_OF_MONTH", IntegerType(), True),
    StructField("DAY_OF_WEEK", IntegerType(), True),
    StructField("FL_DATE", StringType(), True),
    StructField("UNIQUE_CARRIER", StringType(), True),
    StructField("TAIL_NUM", StringType(), True),
    StructField("FL_NUM", IntegerType(), True),
    StructField("ORIGIN_AIRPORT_ID", IntegerType(), True),
    StructField("ORIGIN", StringType(), True),
    StructField("ORIGIN_STATE_ABR", StringType(), True),
    StructField("DEST_AIRPORT_ID", IntegerType(), True),
    StructField("DEST", StringType(), True),
    StructField("DEST_STATE_ABR", StringType(), True),
    StructField("CRS_DEP_TIME", IntegerType(), True),
    StructField("DEP_TIME", IntegerType(), True),
    StructField("DEP_DELAY", DoubleType(), True),
    StructField("DEP_DELAY_NEW", DoubleType(), True),
    StructField("DEP_DEL15", DoubleType(), True),
    StructField("DEP_DELAY_GROUP", IntegerType(), True),
    StructField("TAXI_OUT", DoubleType(), True),
    StructField("WHEELS_OFF", StringType(), True),
    StructField("WHEELS_ON", StringType(), True),
    StructField("TAXI_IN", DoubleType(), True),
    StructField("CRS_ARR_TIME", IntegerType(), True),
    StructField("ARR_TIME", IntegerType(), True),
    StructField("ARR_DELAY", DoubleType(), True),
    StructField("ARR_DELAY_NEW", DoubleType(), True),
    StructField("ARR_DEL15", DoubleType(), True),
    StructField("ARR_DELAY_GROUP", IntegerType(), True),
    StructField("CANCELLED", DoubleType(), True),
    StructField("CANCELLATION_CODE", StringType(), True),
    StructField("DIVERTED", DoubleType(), True),
    StructField("CRS_ELAPSED_TIME", DoubleType(), True),
    StructField("ACTUAL_ELAPSED_TIME", DoubleType(), True),
    StructField("AIR_TIME", DoubleType(), True),
    StructField("FLIGHTS", DoubleType(), True),
    StructField("DISTANCE", DoubleType(), True),
    StructField("DISTANCE_GROUP", IntegerType(), True),
    StructField("CARRIER_DELAY", DoubleType(), True),
    StructField("WEATHER_DELAY", DoubleType(), True),
    StructField("NAS_DELAY", DoubleType(), True),
    StructField("SECURITY_DELAY", DoubleType(), True),
    StructField("LATE_AIRCRAFT_DELAY", DoubleType(), True)])

# COMMAND ----------

dbutils.fs.mkdirs("/mnt/databases/schemas/")
dbutils.fs.rm("/mnt/databases/schemas/airontime_schema.json", True)

with open("/dbfs/mnt/databases/schemas/schema_airontime.json", "w") as f:
    f.write(customSchema.json())