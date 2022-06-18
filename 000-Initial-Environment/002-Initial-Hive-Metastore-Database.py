# Databricks notebook source
# MAGIC %md
# MAGIC # Initial External Hive Metastore Database for Azure SQL Database
# MAGIC **Implement Step:**
# MAGIC * Initial Metastore Database for Azure SQL Database
# MAGIC   * Create Metadata Database<br/>
# MAGIC     **Suggest**: Set database default characters, Example: ***Chinese: Chinese_PRC_CI_AS***
# MAGIC     > Hive Issue: https://issues.apache.org/jira/browse/HIVE-18083<br/>
# MAGIC     > Workaround for character set problems
# MAGIC   * Validation JDK Version for Databricks Runtime
# MAGIC   * Download Apache Hive/ Hadoop and Microsoft SQL Server JDBC Packages<br/>
# MAGIC     **Require**: Match JDK Version - Including their jars build JDK version
# MAGIC   * Copy Microsoft SQL Server JDBC to Hive lib Folder
# MAGIC   * Copy Hadoop Common Lib to Hive lib Folder
# MAGIC   * Use Hive tool ***schematool*** to initial and verify the metadata database
# MAGIC * Set the databricks cluster's parameters and reboot the cluster
# MAGIC * Connect to the exist external metadata database
# MAGIC   * Execute SQL Script: ***SHOW DATABASE*** or pyspark script: ***listDatabases()***
# MAGIC * Configure **cluster policies** for **production environment**
# MAGIC   * Protect sensitive information
# MAGIC   * Deliver connecting to an external Metadata database as a unified standard for cluster creation)

# COMMAND ----------

# MAGIC %sh
# MAGIC java -version

# COMMAND ----------

# MAGIC %md
# MAGIC [Java Platform, Standard Edition 8 Names and Versions](https://www.oracle.com/java/technologies/javase/jdk8-naming.html)
# MAGIC 
# MAGIC ** Version String ** <br/>
# MAGIC Some of Oracle's products expose a version string which is separate from, but related to, the version number. This version string is usually only seen by programs which query the runtime environment, or by users who invoke command line tools. Version strings have the form 1.x, or 1.x.0, where x is the product version number.<br/>
# MAGIC In JDK 8 and JRE 8, the version strings are 1.8 and 1.8.0. Here are some examples where the version string is used:
# MAGIC * java -version (among other information, returns java version "1.8.0")
# MAGIC * java -fullversion (returns java full version "1.8.0-bxx")
# MAGIC * javac -source 1.8 (is an alias for javac -source 8)
# MAGIC * java.version system property
# MAGIC * java.vm.version system property
# MAGIC * @since 1.8 tag values
# MAGIC * jdk1.8.0 installation directory
# MAGIC * jre8 installation directory
# MAGIC 
# MAGIC Oracle periodically makes updates available and, when an update occurs, the version string will also include the update version number. So, JDK 8 update 5, or JDK 8u5, will have the version string "1.8.0_5". When invoking the java -fullversion command, the result also includes the build number, a level of detail not needed by most users.

# COMMAND ----------

# MAGIC %md
# MAGIC [System requirements for the JDBC driver](https://docs.microsoft.com/en-us/sql/connect/jdbc/system-requirements-for-the-jdbc-driver?view=sql-server-ver15)
# MAGIC * Starting with the Microsoft JDBC Driver 4.2 for SQL Server, Java Development Kit (JDK) 8.0 and Java Runtime Environment (JRE) 8.0 are supported. Support for JDBC Spec API has been extended to include the JDBC 4.1 and 4.2 API.
# MAGIC * Starting with the Microsoft JDBC Driver 4.1 for SQL Server, Java Development Kit (JDK) 7.0 and Java Runtime Environment (JRE) 7.0 are supported.
# MAGIC 
# MAGIC ** Microsoft JDBC Driver 9.4 for SQL Server: ** <br/>
# MAGIC The JDBC Driver 9.4 includes three JAR class libraries in each installation package: mssql-jdbc-9.4.0.jre8.jar, mssql-jdbc-9.4.0.jre11.jar, and mssql-jdbc-9.4.0.jre16.jar.<br/>
# MAGIC The JDBC Driver 9.4 is designed to work with and be supported by all major Java virtual machines, but is tested only on OpenJDK 1.8, OpenJDK 11.0, OpenJDK 16.0, Azul Zulu JRE 1.8, Azul Zulu JRE 11.0, and Azul Zulu JRE 16.0.<br/>
# MAGIC The following chart summarizes support provided by the two JAR files included with Microsoft JDBC Drivers 9.4 for SQL Server:<br/>
# MAGIC 
# MAGIC | JAR | JDBC Version Compliance | Recommended Java Version | Description |
# MAGIC | -- | -- | -- | -- |
# MAGIC | mssql-jdbc-9.4.0.jre8.jar | 4.2 | 8 | Requires a Java Runtime Environment (JRE) 1.8. Using JRE 1.7 or lower throws an exception. |
# MAGIC | mssql-jdbc-9.4.0.jre11.jar | 4.3 | 11 | Requires a Java Runtime Environment (JRE) 11.0. Using JRE 10.0 or lower throws an exception. |
# MAGIC | mssql-jdbc-9.4.0.jre16.jar | 4.3 | 16 | Requires a Java Runtime Environment (JRE) 16.0. Using JRE 15.0 or lower throws an exception. |
# MAGIC 
# MAGIC **Issues:**
# MAGIC 1. Exception in thread "main" java.lang.UnsupportedClassVersionError: com/microsoft/sqlserver/jdbc/SQLServerDriver has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0<br/>
# MAGIC **Solved**
# MAGIC <br/>USE MSSQL Server JDBC Version ***9.2***

# COMMAND ----------

# MAGIC %md
# MAGIC [Apache Hadoop 3.3.1](https://hadoop.apache.org/docs/current/)
# MAGIC 
# MAGIC Minimum required Java version increased from Java 7 to Java 8 <br/>
# MAGIC *All Hadoop JARs are now compiled targeting a runtime version of **Java 8***. Users still using Java 7 or below must upgrade to Java 8.

# COMMAND ----------

# MAGIC %sh
# MAGIC wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
# MAGIC wget https://download.microsoft.com/download/b/c/5/bc5e407f-97ff-42ea-959d-12f2391063d7/sqljdbc_9.4.0.0_enu.tar.gz
# MAGIC wget https://downloads.apache.org/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz

# COMMAND ----------

# MAGIC %sh
# MAGIC cp /databricks/driver/hadoop-3.3.1.tar.gz /dbfs/mnt/hivepackages/
# MAGIC cp /databricks/driver/sqljdbc_9.4.0.0_enu.tar.gz /dbfs/mnt/hivepackages/
# MAGIC cp /databricks/driver/apache-hive-3.1.2-bin.tar.gz /dbfs/mnt/hivepackages/
# MAGIC tar -xvzf /dbfs/mnt/hivepackages/hadoop-3.3.1.tar.gz --directory /dbfs/mnt/hivemetastorejars/
# MAGIC tar -xvzf /dbfs/mnt/hivepackages/sqljdbc_9.4.0.0_enu.tar.gz --directory /dbfs/mnt/hivemetastorejars/
# MAGIC tar -xvzf /dbfs/mnt/hivepackages/apache-hive-3.1.2-bin.tar.gz --directory /dbfs/mnt/hivemetastorejars/

# COMMAND ----------

# MAGIC %sh
# MAGIC cp /dbfs/mnt/hivemetastorejars/sqljdbc_9.2/enu/mssql-jdbc-9.2.1.jre8.jar /dbfs/mnt/hivemetastorejars/apache-hive-3.1.2-bin/lib
# MAGIC cp /dbfs/mnt/hivemetastorejars/hadoop-3.3.1/share/hadoop/common/lib/*.jar /dbfs/mnt/hivemetastorejars/apache-hive-3.1.2-bin/lib

# COMMAND ----------

# MAGIC %sh
# MAGIC export HIVE_HOME="/dbfs/mnt/hivemetastorejars/apache-hive-3.1.2-bin/"
# MAGIC export HADOOP_HOME="/dbfs/mnt/hivemetastorejars/hadoop-3.3.1/"
# MAGIC export SQLDB_DRIVER="com.microsoft.sqlserver.jdbc.SQLServerDriver"
# MAGIC export HIVE_URL="jdbc:sqlserver://databricksins.database.chinacloudapi.cn:1433;database=HiveDB;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.chinacloudapi.cn;loginTimeout=30;"
# MAGIC export HIVE_PASSWORD="1qaz@WSX"
# MAGIC export HIVE_USER="hiveadmin"
# MAGIC 
# MAGIC # uncomment following line to init schema
# MAGIC cd $HIVE_HOME
# MAGIC ./bin/schematool -dbType mssql -url $HIVE_URL -passWord $HIVE_PASSWORD -userName $HIVE_USER -driver $SQLDB_DRIVER -initSchema

# COMMAND ----------

# MAGIC %sh
# MAGIC export HIVE_HOME="/dbfs/mnt/hivemetastorejars/apache-hive-3.1.2-bin/"
# MAGIC export HADOOP_HOME="/dbfs/mnt/hivemetastorejars/hadoop-3.3.1/"
# MAGIC export SQLDB_DRIVER="com.microsoft.sqlserver.jdbc.SQLServerDriver"
# MAGIC export HIVE_URL="jdbc:sqlserver://databricksins.database.chinacloudapi.cn:1433;database=HiveDB;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.chinacloudapi.cn;loginTimeout=30;"
# MAGIC export HIVE_PASSWORD="1qaz@WSX"
# MAGIC export HIVE_USER="hiveadmin"
# MAGIC 
# MAGIC # uncomment following line to init schema
# MAGIC cd $HIVE_HOME
# MAGIC ./bin/schematool -dbType mssql -url $HIVE_URL -passWord $HIVE_PASSWORD -userName $HIVE_USER -driver $SQLDB_DRIVER -info

# COMMAND ----------

# MAGIC %md
# MAGIC * Cluster connect to an external's exist metadata database
# MAGIC ```ini
# MAGIC spark.hadoop.javax.jdo.option.ConnectionDriverName com.microsoft.sqlserver.jdbc.SQLServerDriver
# MAGIC spark.hadoop.javax.jdo.option.ConnectionURL jdbc:sqlserver://{databricksins}.database.chinacloudapi.cn:1433;database={Hive211};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.chinacloudapi.cn;loginTimeout=30;
# MAGIC spark.hadoop.javax.jdo.option.ConnectionUserName {hiveadmin}
# MAGIC spark.hadoop.javax.jdo.option.ConnectionPassword {1qaz@WSX}
# MAGIC spark.sql.hive.metastore.version {3.1.2}
# MAGIC spark.sql.hive.metastore.jars {/dbfs/mnt/hivemetastorejars/apache-hive-3.1.2-bin/lib/*}
# MAGIC ```
# MAGIC * For Production Environment
# MAGIC   * Verify metadata version
# MAGIC   * Fixed database schema, NO allow to modify
# MAGIC ```ini
# MAGIC hive.metastore.schema.verification.record.version {true}
# MAGIC datanucleus.fixedDatastore {true}
# MAGIC ```
# MAGIC * Default Cluster Parameters: For High Concurrency Cluster
# MAGIC ```ini
# MAGIC spark.databricks.repl.allowedLanguages sql,python,r
# MAGIC spark.databricks.cluster.profile serverless
# MAGIC spark.databricks.delta.preview.enabled true
# MAGIC ```
# MAGIC * Default Cluster Parameters: For Single Node Cluster
# MAGIC ```ini
# MAGIC spark.master local[*, 4]
# MAGIC spark.databricks.cluster.profile singleNode
# MAGIC spark.databricks.delta.preview.enabled true
# MAGIC ```
# MAGIC * Default Cluster Parameters: For Standard Cluster
# MAGIC ```ini
# MAGIC NO Parameter
# MAGIC ```

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW DATABASES

# COMMAND ----------

spark.catalog.listDatabases()

# COMMAND ----------

# MAGIC %md
# MAGIC * For ***Security Reason***, Deliver parameters by "Cluster Policies", New a policy, give a name for policy and attach json scripts as below:
# MAGIC   * Use Azure Key Vaults to protect ***sensitive information*** such as:
# MAGIC     * Metadata database connection string: Include: Instance Name/ Database Name/ Service Endpoint
# MAGIC     * Database user name
# MAGIC     * Database password
# MAGIC     * Hive common jars path
# MAGIC   * Hide others does not need to be visualized parameters
# MAGIC ```json
# MAGIC {
# MAGIC   "spark_conf.spark.hadoop.javax.jdo.option.ConnectionURL": {
# MAGIC     "type": "fixed",
# MAGIC     "value": "{{secrets/AKV4Databricks/HiveSQLConnectionString}}",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "spark_conf.spark.hadoop.javax.jdo.option.ConnectionDriverName": {
# MAGIC     "type": "fixed",
# MAGIC     "value": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "spark_conf.spark.hadoop.javax.jdo.option.ConnectionUserName": {
# MAGIC     "type": "fixed",
# MAGIC     "value": "{{secrets/AKV4Databricks/HiveSQLUserName}}",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "spark_conf.spark.hadoop.javax.jdo.option.ConnectionPassword": {
# MAGIC     "type": "fixed",
# MAGIC     "value": "{{secrets/AKV4Databricks/HiveSQLPassword}}",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "spark.sql.hive.metastore.version": {
# MAGIC     "type": "unlimited",
# MAGIC     "value": "3.1.2",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "spark.sql.hive.metastore.jars": {
# MAGIC     "type": "unlimited",
# MAGIC     "value": "{{secrets/AKV4Databricks/HiveJarsPath}}",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "hive.metastore.schema.verification.record.version": {
# MAGIC     "type": "unlimited",
# MAGIC     "value": "true",
# MAGIC     "hidden": true
# MAGIC   },
# MAGIC   "datanucleus.fixedDatastore": {
# MAGIC     "type": "unlimited",
# MAGIC     "value": "true",
# MAGIC     "hidden": true
# MAGIC   }
# MAGIC }
# MAGIC ```
# MAGIC * Create/ Edit Cluster's UI's Policy dorpdown list to select your policy name for apply the policy to cluster, and create/start or restart cluster.

# COMMAND ----------

# MAGIC %md
# MAGIC Configure Cluster Policies
# MAGIC ![](https://databricksdocs.blob.core.chinacloudapi.cn/images/InitialExternalHiveMetastore001.png)
# MAGIC ![](https://databricksdocs.blob.core.chinacloudapi.cn/images/InitialExternalHiveMetastore002.png)
# MAGIC ![](https://databricksdocs.blob.core.chinacloudapi.cn/images/InitialExternalHiveMetastore003.png)