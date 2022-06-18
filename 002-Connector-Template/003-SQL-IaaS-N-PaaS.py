# Databricks notebook source
# MAGIC %md
# MAGIC # 定义链接字符串，数据库名，用户名，密码，表名

# COMMAND ----------

Hostname = "xxxx.database.chinacloudapi.cn"
Database = "databaseName"
Port = 1433
username = "userID"
password = "password"
url = "jdbc:sqlserver://{0}:{1};database={2};".format(Hostname, Port, Database)
table_name = "xxx.tableName"

# COMMAND ----------

# MAGIC %md
# MAGIC # 使用 spark connecter 读取目标表，使用 timestamp 进行并行执行

# COMMAND ----------

jdbcDF = spark.read \
        .format("com.microsoft.sqlserver.jdbc.spark") \
        .option("url", url) \
        .option("dbtable", table_name) \
        .option("user", username) \
        .option("password", password) \
        .option("partitionColumn", "partitionColumnName") \
        .option("lowerBound", "2018-01-01 0:00:00") \
        .option("upperBound", "2020-12-31 23:59:59") \
        .option("numPartitions", 1000) \
        .option("timestampFormat", "yyyy-mm-dd") \
        .load().cache()