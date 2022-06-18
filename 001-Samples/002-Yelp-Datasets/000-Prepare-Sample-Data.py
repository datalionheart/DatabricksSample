# Databricks notebook source
# MAGIC %sh
# MAGIC mkdir /dbfs/mnt/rawdata/002-Yelp-Datasets/

# COMMAND ----------

# MAGIC %sh
# MAGIC ls /dbfs/mnt/rawdata/002-Yelp-Datasets/

# COMMAND ----------

# MAGIC %sh
# MAGIC tar -xvf /dbfs/mnt/rawdata/002-Yelp-Datasets/yelp_dataset.tar --directory /dbfs/mnt/rawdata/002-Yelp-Datasets/

# COMMAND ----------

# MAGIC %sh
# MAGIC ls -lh /dbfs/mnt/rawdata/002-Yelp-Datasets/

# COMMAND ----------

df = spark.read.json("/mnt/rawdata/002-Yelp-Datasets/yelp_academic_dataset_user.json")

# COMMAND ----------

df.distinct().select("user_id", "name")

# COMMAND ----------

display(df.distinct().select("user_id", "name"))

# COMMAND ----------

display(df)

# COMMAND ----------

df.schema.simpleString()

# COMMAND ----------

df.createOrReplaceGlobalTempView('users')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from global_temp.users

# COMMAND ----------

df.printSchema()

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC   average_stars,
# MAGIC   compliment_cool,
# MAGIC   compliment_cute,
# MAGIC   compliment_funny,
# MAGIC   compliment_hot,
# MAGIC   compliment_list,
# MAGIC   compliment_more,
# MAGIC   compliment_note,
# MAGIC   compliment_photos,
# MAGIC   compliment_plain,
# MAGIC   compliment_profile,
# MAGIC   compliment_writer,
# MAGIC   cool,
# MAGIC   elite,
# MAGIC   fans,
# MAGIC   explode(split(friends, ", ")) friend,
# MAGIC   funny,
# MAGIC   name,
# MAGIC   review_count,
# MAGIC   useful,
# MAGIC   user_id,
# MAGIC   yelping_since
# MAGIC from
# MAGIC   global_temp.users

# COMMAND ----------

