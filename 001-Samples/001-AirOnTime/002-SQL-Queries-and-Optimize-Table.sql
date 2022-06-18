-- Databricks notebook source
USE AirOnTimeDB

-- COMMAND ----------

select count(1) from AirOnTime

-- COMMAND ----------

select YEAR, MONTH, COUNT(1) from AirOnTime GROUP BY YEAR, MONTH ORDER BY YEAR, MONTH DESC

-- COMMAND ----------

OPTIMIZE AirOnTimeDB.AirOnTime

-- COMMAND ----------

CACHE SELECT * FROM AirOnTime

-- COMMAND ----------

select count(1) from AirOnTime

-- COMMAND ----------

select YEAR, MONTH, COUNT(1) from AirOnTime GROUP BY YEAR, MONTH ORDER BY YEAR, MONTH DESC