# Databricks notebook source
spark.catalog.listDatabases()

# COMMAND ----------

spark.catalog.setCurrentDatabase('airontimedb')
spark.catalog.currentDatabase()

# COMMAND ----------

spark.catalog.listTables()

# COMMAND ----------

spark.catalog.listFunctions()

# COMMAND ----------

spark.catalog.listColumns('airontime')

# COMMAND ----------

spark.catalog.clearCache()

# COMMAND ----------

# MAGIC %sql
# MAGIC USE AirOnTimeDB

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Returns provenance information, including the operation, user, and so on, for each write to a table. Table history is retained for 30 days.
# MAGIC DESCRIBE HISTORY airontime

# COMMAND ----------

# MAGIC %sql
# MAGIC -- You can retrieve detailed information about a Delta table (for example, number of files, data size) using DESCRIBE DETAIL.
# MAGIC DESCRIBE DETAIL airontime

# COMMAND ----------

# MAGIC %md
# MAGIC * **Data retention**
# MAGIC To time travel to a previous version, you must retain both the log and the data files for that version.
# MAGIC 
# MAGIC The data files backing a Delta table are **never** deleted automatically; data files are deleted only **when you run VACUUM**. <br/>
# MAGIC VACUUM **does not** delete Delta log files; log files are **automatically cleaned up** after checkpoints are written.
# MAGIC 
# MAGIC By default you can time travel to a Delta table up to **30 days** old unless you have:
# MAGIC * Run VACUUM on your Delta table.
# MAGIC 
# MAGIC * Changed the data or log file retention periods using the following table properties:
# MAGIC 
# MAGIC   * delta.logRetentionDuration = "interval <interval>": controls how long the history for a table is kept. The default is interval 30 days.<br/>
# MAGIC Each time a checkpoint is written, Databricks automatically cleans up log entries older than the retention interval. If you set this config to a large enough value, many log entries are retained. This should not impact performance as operations against the log are constant time. Operations on history are parallel but will become more expensive as the log size increases.
# MAGIC 
# MAGIC   * delta.deletedFileRetentionDuration = "interval <interval>": controls how long ago a file must have been deleted before being a candidate for VACUUM. The default is interval 7 days.<br/>To access 30 days of historical data even if you run VACUUM on the Delta table, set delta.deletedFileRetentionDuration = "interval 30 days". This setting may cause your storage costs to go up.
# MAGIC 
# MAGIC * **Important**:
# MAGIC   * **vacuum** deletes only data files, not log files. Log files are deleted automatically and asynchronously after checkpoint operations. The default retention period of log files is **30 days**, configurable through the delta.logRetentionDuration property which you set with the ALTER TABLE SET TBLPROPERTIES SQL method. See Table properties.
# MAGIC   * The ability to time travel back to a version older than the retention period is lost after running **vacuum**.

# COMMAND ----------

spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", False)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- VACUUM table_identifier [RETAIN num HOURS] [DRY RUN]
# MAGIC VACUUM airontime RETAIN 24 HOURS DRY RUN

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM airontime RETAIN 24 HOURS

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Python: spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", True)
# MAGIC SET spark.databricks.delta.retentionDurationCheck.enabled = True

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY airontime

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(1) from airontime

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY airontime