# Databricks notebook source
# MAGIC %md
# MAGIC * [Azure EventHub Driver](https://github.com/Azure/azure-event-hubs-spark)
# MAGIC * [pyspark sample & parameters](https://github.com/Azure/azure-event-hubs-spark/blob/master/docs/PySpark/structured-streaming-pyspark.md)

# COMMAND ----------

import datetime
import json

# End at the current time. This datetime formatting creates the correct string format from a python datetime object
# Start from beginning of stream
startOffset = "-1"
endTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# Get Eventhub connection string
connectionString = "Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=Consumer;SharedAccessKey=UxvwoFGIHTLlE/MZyOsMhX2U8yglLlcvZBygf2biV9Q=;EntityPath=datasim"

# Create the positions
startingEventPosition = {
  "offset": startOffset,  
  "seqNo": -1,            #not in use
  "enqueuedTime": None,   #not in use
  "isInclusive": True
}

endingEventPosition = {
  "offset": None,           #not in use
  "seqNo": -1,              #not in use
  "enqueuedTime": endTime,
  "isInclusive": True
}

# Put the positions into the Event Hub config dictionary
ehConf = {}
ehConf['eventhubs.connectionString'] = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString)
ehConf["eventhubs.startingPosition"] = json.dumps(startingEventPosition)
ehConf["eventhubs.endingPosition"] = json.dumps(endingEventPosition)
ehConf['eventhubs.consumerGroup'] = "$Default"

# COMMAND ----------

# Simple batch query
df = spark \
  .readStream \
  .format("eventhubs") \
  .options(**ehConf) \
  .load()

# COMMAND ----------

readInStreamBody = df.withColumn("body", df["body"].cast("string"))
display(readInStreamBody)