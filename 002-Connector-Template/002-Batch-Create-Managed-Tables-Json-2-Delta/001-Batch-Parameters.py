# Databricks notebook source
# MAGIC %sh
# MAGIC ls /dbfs/mnt/stagedata/002-Yelp-Datasets/*.json

# COMMAND ----------

fileInfo = dbutils.fs.ls("dbfs:/mnt/stagedata/002-Yelp-Datasets/")

# COMMAND ----------

import numpy as np
fileNames = np.array(fileInfo)[:,1]

# COMMAND ----------

fileNames = [fileName for fileName in fileNames if fileName not in set(["json"])]

# COMMAND ----------

fileNames

# COMMAND ----------

# MAGIC %scala
# MAGIC dbutils.fs.ls("dbfs:/mnt/stagedata/002-Yelp-Datasets").map(_.name).filter(x=>x.contains("json"))

# COMMAND ----------

fileInfo[1:]

# COMMAND ----------

filter('*.json', dbutils.fs.ls("dbfs:/mnt/stagedata/002-Yelp-Datasets/"))

# COMMAND ----------

import numpy as np
np.array(fileInfo)[1:,1]

# COMMAND ----------

filePrefix = '/dbfs/mnt/stagedata/002-Yelp-Datasets/yelp_academic_dataset_'

# COMMAND ----------

tableNames = ['', '', '']