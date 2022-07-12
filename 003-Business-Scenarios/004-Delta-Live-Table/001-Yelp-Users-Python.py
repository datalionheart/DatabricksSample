# Databricks notebook source
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

json_path = "/mnt/rawdata/002-Yelp-Datasets/users/"
@dlt.create_table(
  comment="The raw users dataset, ingested from /mnt/rawdata/002-Yelp-Datasets."
)
def users_raw():          
  return (
    spark.readStream.format("cloudFiles")
      .option("cloudFiles.format", "json")
      .load(json_path)
  )

# COMMAND ----------

@dlt.table(
  comment="users data cleaned and prepared for analysis."
)
@dlt.expect("yelping_since", "yelping_since IS NOT NULL")
def users_prepared():
  return (
    dlt.read_stream("users_raw")
      .withColumn("friend", explode(split(col('friends'), ", ")))
      .select("user_id", "friend", "name", "fans", "yelping_since")
  )

# COMMAND ----------

@dlt.table(
  comment="Convert users to friendship."
)
@dlt.expect_or_fail("user_id", "user_id IS NOT NULL")
def friendship():
  return (
    dlt.read("users_prepared")
      .distinct()
      .select("user_id", "friend")
  )

# COMMAND ----------

@dlt.table(
  comment="Filter hot users"
)
@dlt.expect_or_drop("fans", "fans < 10")
def hot_users():
  return (
    dlt.read("users_prepared")
      .distinct()
      .select("user_id", "name", "fans")
  )