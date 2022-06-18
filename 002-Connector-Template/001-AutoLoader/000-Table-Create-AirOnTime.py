# Databricks notebook source
# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS airontimedb.airontime_streaming_001

# COMMAND ----------

dbutils.fs.rm("dbfs:/mnt/databases/airontimedb/airontime_streaming_001", recurse=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS airontimedb.airontime_streaming_001
# MAGIC   (YEAR   integer,
# MAGIC   MONTH   integer,
# MAGIC   DAY_OF_MONTH   integer,
# MAGIC   DAY_OF_WEEK   integer,
# MAGIC   FL_DATE   string,
# MAGIC   UNIQUE_CARRIER   string,
# MAGIC   TAIL_NUM   string,
# MAGIC   FL_NUM   integer,
# MAGIC   ORIGIN_AIRPORT_ID   integer,
# MAGIC   ORIGIN   string,
# MAGIC   ORIGIN_STATE_ABR   string,
# MAGIC   DEST_AIRPORT_ID   integer,
# MAGIC   DEST   string,
# MAGIC   DEST_STATE_ABR   string,
# MAGIC   CRS_DEP_TIME   integer,
# MAGIC   DEP_TIME   integer,
# MAGIC   DEP_DELAY   double,
# MAGIC   DEP_DELAY_NEW   double,
# MAGIC   DEP_DEL15   double,
# MAGIC   DEP_DELAY_GROUP   integer,
# MAGIC   TAXI_OUT   double,
# MAGIC   WHEELS_OFF   string,
# MAGIC   WHEELS_ON   string,
# MAGIC   TAXI_IN   double,
# MAGIC   CRS_ARR_TIME   integer,
# MAGIC   ARR_TIME   integer,
# MAGIC   ARR_DELAY   double,
# MAGIC   ARR_DELAY_NEW   double,
# MAGIC   ARR_DEL15   double,
# MAGIC   ARR_DELAY_GROUP   integer,
# MAGIC   CANCELLED   double,
# MAGIC   CANCELLATION_CODE   string,
# MAGIC   DIVERTED   double,
# MAGIC   CRS_ELAPSED_TIME   double,
# MAGIC   ACTUAL_ELAPSED_TIME   double,
# MAGIC   AIR_TIME   double,
# MAGIC   FLIGHTS   double,
# MAGIC   DISTANCE   double,
# MAGIC   DISTANCE_GROUP   integer,
# MAGIC   CARRIER_DELAY   double,
# MAGIC   WEATHER_DELAY   double,
# MAGIC   NAS_DELAY   double,
# MAGIC   SECURITY_DELAY   double,
# MAGIC   LATE_AIRCRAFT_DELAY   double)
# MAGIC USING DELTA
# MAGIC PARTITIONED BY (YEAR)
# MAGIC LOCATION "dbfs:/mnt/databases/airontimedb/airontime_streaming_001"
# MAGIC TBLPROPERTIES (
# MAGIC   delta.autoOptimize.optimizeWrite = true, 
# MAGIC   delta.autoOptimize.autoCompact = true)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE EXTENDED airontimedb.airontime_streaming_001