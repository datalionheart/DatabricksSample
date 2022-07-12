-- Databricks notebook source
-- MAGIC %python
-- MAGIC import datetime
-- MAGIC datetime.datetime.now()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC spark.conf.set("spark.sql.session.timeZone", "Asia/Shanghai")
-- MAGIC import datetime
-- MAGIC datetime.datetime.now()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC spark.conf.set("spark.sql.session.timeZone", "CST")
-- MAGIC 
-- MAGIC import datetime
-- MAGIC datetime.datetime.now()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import pytz
-- MAGIC import datetime
-- MAGIC 
-- MAGIC tz = pytz.timezone("Asia/Shanghai")
-- MAGIC print(tz.localize(datetime.datetime.now()))

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from datetime import timedelta

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import datetime
-- MAGIC datetime.datetime.now

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import time
-- MAGIC time.localtime()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import time
-- MAGIC time.timezone

-- COMMAND ----------

-- MAGIC %python
-- MAGIC import pytz
-- MAGIC # pytz.all_timezones
-- MAGIC # pytz.common_timezones
-- MAGIC # pytz.country_timezones
-- MAGIC 
-- MAGIC print('CN TimeZones')
-- MAGIC for timeZone in pytz.country_timezones['CN']:
-- MAGIC     print(timeZone)
-- MAGIC 
-- MAGIC # ISO Alpha 2
-- MAGIC # for code, name in pytz.country_names.items():
-- MAGIC #     print(code, ':', name)

-- COMMAND ----------

SELECT current_timezone();

-- COMMAND ----------

SELECT now()

-- COMMAND ----------

-- Set time zone to the region-based zone ID.
SET spark.sql.session.timeZone = Asia/Shanghai
> SET timezone = America/Los_Angeles;
> SELECT current_timezone();
  America/Los_Angeles

-- COMMAND ----------

-- Set time zone to the Zone offset.
> SET timezone = +08:00;
> SELECT current_timezone();
  +08:00