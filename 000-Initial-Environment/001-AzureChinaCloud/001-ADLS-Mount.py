# Databricks notebook source
# MAGIC %run ../000-Initial-Parameters

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope=AzureKeyVaultScopeName,key="ApplicationID-ADLS4Databricks"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope=AzureKeyVaultScopeName,key="ADLS4DatabricksSecrets"),
           "fs.azure.account.oauth2.client.endpoint": "https://login.partner.microsoftonline.cn/" + dbutils.secrets.get(scope=AzureKeyVaultScopeName,key="TenantDirectoryID") + "/oauth2/token"}

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.chinacloudapi.cn/".format("adls4dscores", "rawdata"),
  mount_point = "/mnt/rawdata",
  extra_configs = configs)

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.chinacloudapi.cn/".format("adls4dscores", "stagedata"),
  mount_point = "/mnt/stagedata",
  extra_configs = configs)

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.chinacloudapi.cn/".format("adls4dscores", "databases"),
  mount_point = "/mnt/databases",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.chinacloudapi.cn/".format("hivemetastorejarsstorage", "hivepackages"),
  mount_point = "/mnt/hivepackages",
  extra_configs = configs)

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.chinacloudapi.cn/".format("hivemetastorejarsstorage", "hivemetastorejars"),
  mount_point = "/mnt/hivemetastorejars",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.refreshMounts()

# COMMAND ----------

dbutils.fs.ls('dbfs:/mnt/')