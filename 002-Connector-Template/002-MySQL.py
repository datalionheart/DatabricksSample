# Databricks notebook source
# MAGIC %sh nc -vz 192.168.0.4 3306

# COMMAND ----------

# MAGIC %md
# MAGIC From oracle offical website download mysql driver and upload to databricks workspace then install it to cluster

# COMMAND ----------

jdbcHostname = "192.168.0.4"
jdbcDatabase = "sgspoc"
jdbcPort = 3306
jdbcUsername = "sqladmin"
jdbcPassword = "!QAZ2wsx#EDC"

jdbcUrl = "jdbc:mysql://{0}:{1}/{2}?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC".format(jdbcHostname, jdbcPort, jdbcDatabase)
connectionProperties = {
  "user" : jdbcUsername,
  "password" : jdbcPassword,
  "driver" : "com.mysql.jdbc.Driver"
}

# COMMAND ----------

pushdown_query = "(select * from tableName) tableAlias"
df = spark.read.jdbc(url=jdbcUrl, table=pushdown_query, properties=connectionProperties).cache()