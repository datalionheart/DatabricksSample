# Databricks notebook source
dfYellow = spark.read.parquet('/mnt/rawdata/nyctlc/yellow/*')

# COMMAND ----------

dfGreen = spark.read.parquet('/mnt/rawdata/nyctlc/green/*')

# COMMAND ----------

dfFHV = spark.read.parquet('/mnt/rawdata/nyctlc/fhv/*')

# COMMAND ----------

dfYellow.createOrReplaceGlobalTempView('yellow_texi')

# COMMAND ----------

dfGreen.createOrReplaceGlobalTempView('green_texi')

# COMMAND ----------

dfFHV.createOrReplaceGlobalTempView('fhv_texi')

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC   date_format(tpep_pickup_datetime, 'yyyy-MM') pickup_month
# MAGIC from global_temp.yellow_texi
# MAGIC union all
# MAGIC select
# MAGIC   date_format(lpep_pickup_datetime, 'yyyy-MM') pickup_month
# MAGIC from global_temp.green_texi
# MAGIC union all
# MAGIC select
# MAGIC   date_format(pickup_datetime, 'yyyy-MM') pickup_month
# MAGIC from global_temp.fhv_texi

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(1), a.pickup_month, a.type from (
# MAGIC   select
# MAGIC     date_format(tpep_pickup_datetime, 'yyyy-MM') pickup_month
# MAGIC     ,'yellow' type
# MAGIC   from global_temp.yellow_texi
# MAGIC   union all
# MAGIC   select
# MAGIC     date_format(lpep_pickup_datetime, 'yyyy-MM') pickup_month
# MAGIC     ,'green' type
# MAGIC   from global_temp.green_texi
# MAGIC   union all
# MAGIC   select
# MAGIC     date_format(pickup_datetime, 'yyyy-MM') pickup_month
# MAGIC     ,'fhv' type
# MAGIC   from global_temp.fhv_texi) a
# MAGIC group by a.pickup_month, a.type
# MAGIC having a.pickup_month between '2011-01-01' and '2022-02-01'
# MAGIC order by a.pickup_month