# Databricks notebook source
# MAGIC %md
# MAGIC [TLC Trip Record Data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

# COMMAND ----------

# MAGIC %sh
# MAGIC mkdir /dbfs/mnt/rawdata/nyctlc
# MAGIC mkdir /dbfs/mnt/rawdata/nyctlc/yellow
# MAGIC mkdir /dbfs/mnt/rawdata/nyctlc/green
# MAGIC mkdir /dbfs/mnt/rawdata/nyctlc/fhv
# MAGIC mkdir /dbfs/mnt/rawdata/nyctlc/fhvhv

# COMMAND ----------

import urllib.request
from datetime import datetime

url = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2021-01.parquet"
fileName = url.split("/")[-1]
fullFileName = "/dbfs/mnt/rawdata/nyctlc/yellow/{0}".format(fileName)

try:
    urllib.request.urlretrieve(url, fullFileName)
except Exception as exc:
    print(f"urlretrieve failed: {str(exc)}")

# COMMAND ----------

import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
endDate='2022/02/01'
beginDate='2009/01/01'

countMonth=(datetime.strptime(endDate, '%Y/%m/%d').year - datetime.strptime(beginDate, '%Y/%m/%d').year) * 12 \
            + datetime.strptime(endDate, '%Y/%m/%d').month

for i in range(0, countMonth):
    compute_date = datetime.strptime(beginDate, '%Y/%m/%d') + relativedelta(months=i)
    url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_{0}.parquet'.format(compute_date.strftime('%Y-%m'))
    fileName = url.split("/")[-1]
    fullFileName = '/dbfs/mnt/rawdata/nyctlc/yellow/{0}'.format(fileName)
    try:
        urllib.request.urlretrieve(url, fullFileName)
        print('Download {0} Done.'.format(fileName))
    except Exception as exc:
        print(f"{fileName} failed: {str(exc)}")

# COMMAND ----------

import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
endDate='2022/02/01'
beginDate='2009/01/01'

countMonth=(datetime.strptime(endDate, '%Y/%m/%d').year - datetime.strptime(beginDate, '%Y/%m/%d').year) * 12 \
            + datetime.strptime(endDate, '%Y/%m/%d').month

for i in range(0, countMonth):
    compute_date = datetime.strptime(beginDate, '%Y/%m/%d') + relativedelta(months=i)
    url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/green_tripdata_{0}.parquet'.format(compute_date.strftime('%Y-%m'))
    fileName = url.split("/")[-1]
    fullFileName = '/dbfs/mnt/rawdata/nyctlc/green/{0}'.format(fileName)
    try:
        urllib.request.urlretrieve(url, fullFileName)
        print('Download {0} Done.'.format(fileName))
    except Exception as exc:
        print(f"{fileName} failed: {str(exc)}")

# COMMAND ----------

import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
endDate='2022/02/01'
beginDate='2009/01/01'

countMonth=(datetime.strptime(endDate, '%Y/%m/%d').year - datetime.strptime(beginDate, '%Y/%m/%d').year) * 12 \
            + datetime.strptime(endDate, '%Y/%m/%d').month

for i in range(0, countMonth):
    compute_date = datetime.strptime(beginDate, '%Y/%m/%d') + relativedelta(months=i)
    url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_{0}.parquet'.format(compute_date.strftime('%Y-%m'))
    fileName = url.split("/")[-1]
    fullFileName = '/dbfs/mnt/rawdata/nyctlc/fhv/{0}'.format(fileName)
    try:
        urllib.request.urlretrieve(url, fullFileName)
        print('Download {0} Done.'.format(fileName))
    except Exception as exc:
        print(f"{fileName} failed: {str(exc)}")

# COMMAND ----------

import urllib.request
from datetime import datetime
from dateutil.relativedelta import relativedelta
endDate='2022/02/01'
beginDate='2009/01/01'

countMonth=(datetime.strptime(endDate, '%Y/%m/%d').year - datetime.strptime(beginDate, '%Y/%m/%d').year) * 12 \
            + datetime.strptime(endDate, '%Y/%m/%d').month

for i in range(0, countMonth):
    compute_date = datetime.strptime(beginDate, '%Y/%m/%d') + relativedelta(months=i)
    url = 'https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_{0}.parquet'.format(compute_date.strftime('%Y-%m'))
    fileName = url.split("/")[-1]
    fullFileName = '/dbfs/mnt/rawdata/nyctlc/fhvhv/{0}'.format(fileName)
    try:
        urllib.request.urlretrieve(url, fullFileName)
        print('Download {0} Done.'.format(fileName))
    except Exception as exc:
        print(f"{fileName} failed: {str(exc)}")