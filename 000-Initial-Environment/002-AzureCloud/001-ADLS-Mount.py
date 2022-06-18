# Databricks notebook source
# MAGIC %run ../000-Initial-Parameters

# COMMAND ----------

# MAGIC %md
# MAGIC # Official Document
# MAGIC [National clouds](https://docs.microsoft.com/en-us/azure/active-directory/develop/authentication-national-cloud)
# MAGIC | National cloud | Azure portal endpoint |
# MAGIC | --- | --- |
# MAGIC | Azure portal China operated by 21Vianet | https://login.partner.microsoftonline.cn |
# MAGIC | Azure AD (global service) | https://login.microsoftonline.com |
# MAGIC 
# MAGIC * Authorization common endpoint is: https://***Azure portal endpoint***/common/oauth2/v2.0/authorize
# MAGIC * Token common endpoint is: https://***Azure portal endpoint***/common/oauth2/v2.0/token
# MAGIC 
# MAGIC > ***common*** can be replace ***tenant ID***

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope=AzureKeyVaultScopeName,key="DatabricksAppsID"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope=AzureKeyVaultScopeName,key="DatabricksAppsSecrets"),
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/" + dbutils.secrets.get(scope=AzureKeyVaultScopeName,key="TenantDirectoryID") + "/oauth2/token"}

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.windows.net/".format("adls4databricks", "rawdata"),
  mount_point = "/mnt/rawdata",
  extra_configs = configs)

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.windows.net/".format("adls4databricks", "stagedata"),
  mount_point = "/mnt/stagedata",
  extra_configs = configs)

dbutils.fs.mount(
  source = "abfss://{1}@{0}.dfs.core.windows.net/".format("adls4databricks", "databases"),
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

# MAGIC %sh
# MAGIC ls -lh /dbfs/mnt/rawdata/

# COMMAND ----------

dbutils.fs.ls('dbfs:/mnt/')

# COMMAND ----------

dbutils.fs.unmount('/mnt/rawdata')
dbutils.fs.unmount('/mnt/stagedata')
dbutils.fs.unmount('/mnt/databases')