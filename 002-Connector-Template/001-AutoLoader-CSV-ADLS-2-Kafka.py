# Databricks notebook source
# MAGIC %md
# MAGIC * Schema on READ
# MAGIC   * Predefined schema on notebook as parameters to use to AutoLoader(option: schema)

# COMMAND ----------

spark.conf.set("spark.databricks.cloudFiles.schemaInference.sampleSize.numBytes", "256mb")
spark.conf.set("spark.databricks.cloudFiles.schemaInference.sampleSize.numFiles", "1")

# COMMAND ----------

# MAGIC %run ./001-AutoLoader/000-Schema-AirOnTime

# COMMAND ----------

df = spark.readStream.format("cloudFiles") \
        .option("cloudFiles.format", "csv") \
        .option("header", "true") \
        .schema(customSchema) \
        .load("dbfs:/mnt/rawdata/001-AirOnTime/*.csv")

# COMMAND ----------

EH_SASL = 'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="Endpoint=sb://ehns-databricks.servicebus.chinacloudapi.cn/;SharedAccessKeyName=databircks-admin;SharedAccessKey=i0drtFiipx47hogHhFgj3/id5dHPa3dKw2zhsi455do=";'
print(EH_SASL)

# COMMAND ----------

from pyspark.sql.functions import *

df.select(to_json(struct("*")).alias("value")) \
  .selectExpr("CAST(value AS STRING)") \
  .writeStream \
  .queryName("AutoLoader-From-ADLS-ETL-AirOnTime-2-Kafka") \
  .format("kafka") \
  .option("topic", "eh-databricks-learning") \
  .option("kafka.sasl.mechanism", "PLAIN") \
  .option("kafka.security.protocol", "SASL_SSL") \
  .option("kafka.sasl.jaas.config", EH_SASL) \
  .option("kafka.bootstrap.servers", "ehns-databricks.servicebus.chinacloudapi.cn:9093") \
  .option("checkpointLocation", "dbfs:/mnt/rawdata/kafka/_checkpoint/") \
  .start()

# COMMAND ----------

# OAuth2
bootstrap.servers=NAMESPACENAME.servicebus.windows.net:9093
security.protocol=SASL_SSL
sasl.mechanism=OAUTHBEARER
sasl.jaas.config=org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;
sasl.login.callback.handler.class=CustomAuthenticateCallbackHandler

# SAS
bootstrap.servers=NAMESPACENAME.servicebus.windows.net:9093
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
EH_SASL = 'org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="Endpoint=sb://ehns-databricks.servicebus.chinacloudapi.cn/;SharedAccessKeyName=databricks-send;SharedAccessKey=hyq5sZ98AnSH8DEtyqkSsJiBWkFDHXO3eCb9Aow+Ims=;EntityPath=eh-databricks-learning";'
print(EH_SASL)

# COMMAND ----------

from pyspark.sql.functions import *

df.select(to_json(struct("*")).alias("value")) \
  .selectExpr("CAST(value AS STRING)") \
  .writeStream \
  .queryName("AutoLoader-From-ADLS-ETL-AirOnTime-2-Kafka") \
  .format("kafka") \
  .option("kafka.sasl.mechanism", "PLAIN") \
  .option("kafka.security.protocol", "SASL_SSL") \
  .option("kafka.sasl.jaas.config", EH_SASL) \
  .option("kafka.batch.size", 5000) \
  .option("kafka.bootstrap.servers", "ehns-databricks.servicebus.chinacloudapi.cn:9093") \
  .option("kafka.request.timeout.ms", 120000) \
  .option("topic", "databricks") \
  .option("checkpointLocation", "dbfs:/mnt/rawdata/kafka/_checkpoint/") \
  .start()