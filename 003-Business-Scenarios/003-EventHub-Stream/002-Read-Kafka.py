# Databricks notebook source
kafka = spark \
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", "ehdebezcdc.servicebus.windows.net:9093") \
      .option("subscribe", "datasim") \
      .option("startingOffsets", "latest") \
      .option("kafka.security.protocol","SASL_SSL") \
      .option("kafka.sasl.mechanism", "PLAIN") \
      .option("kafka.sasl.jaas.config", """kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=Consumer;SharedAccessKey=UxvwoFGIHTLlE/MZyOsMhX2U8yglLlcvZBygf2biV9Q=;EntityPath=datasim";""").load()

# COMMAND ----------

from pyspark.sql.functions import get_json_object, col, regexp_replace, concat, lit, to_json
kafka = kafka.select(col("value").cast("string"))

# COMMAND ----------

kafka.createOrReplaceGlobalTempView('kafkademo')

# COMMAND ----------

display(kafka)

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC   get_json_object(value, "$.CountryCode") Country,
# MAGIC   get_json_object(value, "$.RandomValue") RandomValue
# MAGIC from
# MAGIC   GLOBAL_temp.kafkademo