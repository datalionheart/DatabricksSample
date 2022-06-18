-- Databricks notebook source
CREATE DATABASE IF NOT EXISTS AirOnTimeDB LOCATION 'dbfs:/mnt/databases/airontimedb'

-- COMMAND ----------

DESCRIBE DATABASE EXTENDED AirOnTimeDB

-- COMMAND ----------

CREATE DATABASE IF NOT EXISTS YelpAcademicDataset LOCATION 'dbfs:/mnt/databases/yelp_academic_dataset'

-- COMMAND ----------

DESCRIBE DATABASE EXTENDED YelpAcademicDataset