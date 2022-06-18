-- Databricks notebook source
USE AirOnTimeDB

-- COMMAND ----------

ALTER TABLE AirOnTime
SET TBLPROPERTIES
('created.by.user' = 'Jacky Tang', 
'created.date' = '10-16-2021',
delta.autoOptimize.optimizeWrite = true, 
delta.autoOptimize.autoCompact = true)