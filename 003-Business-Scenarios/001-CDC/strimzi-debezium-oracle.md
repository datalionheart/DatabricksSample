# Azure-Based Oracle CDC Open Source Solution

`debezium CDC connector for oracle` 

`strimzi kafka cluster` `strizmi kafka zookeeper cluster` `strimzi kafka connect cluster`

`azure kubernetes services` `oracle 19c CDB/PDB` `oracle logminer`

[TOC]

# Prepare oracle for debezium

## Oracle listener services ready

```bash
lsnrctl services
--- result ---
LSNRCTL for 64-bit Windows: Version 19.0.0.0.0 - Production on 10-JUL-2022 20:13:58

Copyright (c) 1991, 2019, Oracle.  All rights reserved.

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=WINORC19.bjiovdbxfvkejfvdeeiz4oopug.hx.internal.cloudapp.net)(PORT=1521)))
Services Summary...
Service "52448234712340b69f274bcc790ecfe0" has 1 instance(s).
  Instance "orclcdb", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:0 refused:0 state:ready
         LOCAL SERVER
Service "CLRExtProc" has 1 instance(s).
  Instance "CLRExtProc", status UNKNOWN, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:0 refused:0
         LOCAL SERVER
Service "c1d3fc8ac0bc4f91a4f42974b517303e" has 1 instance(s).
  Instance "orclcdb", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:0 refused:0 state:ready
         LOCAL SERVER
Service "orclcdb" has 1 instance(s).
  Instance "orclcdb", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:0 refused:0 state:ready
         LOCAL SERVER
Service "orclcdbXDB" has 1 instance(s).
  Instance "orclcdb", status READY, has 1 handler(s) for this service...
    Handler(s):
      "D000" established:0 refused:0 current:0 max:1022 state:ready
         DISPATCHER <machine: WINORC19, pid: 5512>
         (ADDRESS=(PROTOCOL=tcp)(HOST=WINORC19)(PORT=50429))
Service "orclpdb" has 1 instance(s).
  Instance "orclcdb", status READY, has 1 handler(s) for this service...
    Handler(s):
      "DEDICATED" established:0 refused:0 state:ready
         LOCAL SERVER
The command completed successfully
```

## Configure TNSNames

```bash
run netca
--- result ---
Oracle Net Services Configuration:
Default local naming configuration complete.
    Created net service name: orclcdb
Default local naming configuration complete.
    Created net service name: orclpdb
Oracle Net Services configuration successful. The exit code is 0
--- end ---

or add contents to file tnsnames.ora
--- Add ---
ORCLCDB =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.70)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVICE_NAME = orclcdb)
    )
  )

ORCLPDB =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.70)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVICE_NAME = orclpdb)
    )
  )
--- end ---
```

## Oracle Archive and LogMiner Configure

```plsql
sqlplus sys/oracle as sysdba
alter system set db_recovery_file_dest_size = 10G;
alter system set db_recovery_file_dest = 'C:\oracle\app\fast_recovery_area' scope=spfile;
shutdown immediate
startup mount
alter database archivelog;
alter database open;
archive log list
--- result ---
Database log mode              Archive Mode
Automatic archival             Enabled
Archive destination            USE_DB_RECOVERY_FILE_DEST
Oldest online log sequence     1
Next log sequence to archive   2
Current log sequence           2
--- end ---
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;
exit

sqlplus sys/oracle@//192.168.1.70:1521/orclcdb as sysdba
CREATE TABLESPACE logminer_tbs DATAFILE 'C:\oracle\app\oradata\ORCLCDB\logminer_tbs.dbf' SIZE 25M REUSE AUTOEXTEND ON MAXSIZE UNLIMITED;
exit;

mkdir C:\oracle\app\oradata\ORCLCDB\ORCLPDB
sqlplus sys/oracle@//192.168.1.70:1521/orclpdb as sysdba
ALTER DATABASE OPEN;
CREATE TABLESPACE logminer_tbs DATAFILE 'C:\oracle\app\oradata\ORCLCDB\ORCLPDB\logminer_tbs.dbf' SIZE 25M REUSE AUTOEXTEND ON MAXSIZE UNLIMITED;
exit;

sqlplus sys/oracle@//192.168.1.70:1521/orclcdb as sysdba
CREATE USER c##dbzuser IDENTIFIED BY dbz DEFAULT TABLESPACE logminer_tbs QUOTA UNLIMITED ON logminer_tbs CONTAINER=ALL;
GRANT CREATE SESSION TO c##dbzuser CONTAINER=ALL;
GRANT SET CONTAINER TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$DATABASE to c##dbzuser CONTAINER=ALL;
GRANT FLASHBACK ANY TABLE TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ANY TABLE TO c##dbzuser CONTAINER=ALL;
GRANT SELECT_CATALOG_ROLE TO c##dbzuser CONTAINER=ALL;
GRANT EXECUTE_CATALOG_ROLE TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ANY TRANSACTION TO c##dbzuser CONTAINER=ALL;
GRANT LOGMINING TO c##dbzuser CONTAINER=ALL;
GRANT CREATE TABLE TO c##dbzuser CONTAINER=ALL;
GRANT LOCK ANY TABLE TO c##dbzuser CONTAINER=ALL;
GRANT CREATE SEQUENCE TO c##dbzuser CONTAINER=ALL;
GRANT EXECUTE ON DBMS_LOGMNR TO c##dbzuser CONTAINER=ALL;
GRANT EXECUTE ON DBMS_LOGMNR_D TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$LOG TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$LOG_HISTORY TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$LOGMNR_LOGS TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$LOGMNR_CONTENTS TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$LOGMNR_PARAMETERS TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$LOGFILE TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$ARCHIVED_LOG TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$ARCHIVE_DEST_STATUS TO c##dbzuser CONTAINER=ALL;
GRANT SELECT ON V_$TRANSACTION TO c##dbzuser CONTAINER=ALL;
```

## Verify LogMiner

```pl
SELECT member FROM v$logfile;
--- result ---
C:\ORACLE\APP\FAST_RECOVERY_AREA\ORCLCDB\ONLINELOG\O1_MF_3_KDOHNXGQ_.LOG
C:\ORACLE\APP\FAST_RECOVERY_AREA\ORCLCDB\ONLINELOG\O1_MF_2_KDOHNXGQ_.LOG
C:\ORACLE\APP\FAST_RECOVERY_AREA\ORCLCDB\ONLINELOG\O1_MF_1_KDOHNX9T_.LOG
--- end ---

execute dbms_logmnr.add_logfile('C:\ORACLE\APP\FAST_RECOVERY_AREA\ORCLCDB\ONLINELOG\O1_MF_3_KDOHNXGQ_.LOG',dbms_logmnr.new);
execute dbms_logmnr.add_logfile('C:\ORACLE\APP\FAST_RECOVERY_AREA\ORCLCDB\ONLINELOG\O1_MF_2_KDOHNXGQ_.LOG',dbms_logmnr.addfile);
execute dbms_logmnr.add_logfile('C:\ORACLE\APP\FAST_RECOVERY_AREA\ORCLCDB\ONLINELOG\O1_MF_1_KDOHNX9T_.LOG',dbms_logmnr.addfile);
execute dbms_logmnr.start_logmnr(options=>dbms_logmnr.dict_from_online_catalog+dbms_logmnr.committed_data_only);
select sql_redo,sql_undo from v$logmnr_contents where table_name like '%TAB%' and OPERATION='INSERT';
execute dbms_logmnr.end_logmnr;
```

# Install tools

 `kubectl` `azure cli` `docker engine`

## kubectl
```bash
mkdir tools
cd tools
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl

vi .bashrc
TOOLS_HOME=/root/tools
export PATH=$PATH:$TOOLS_HOME

source .bashrc
```

## azure cli
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## docker engine
```bash
apt-get remove docker docker-engine docker.io containerd runc
apt-get update
apt-get install ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io
docker run hello-world
```

# Connect to Azure Kubernetes Cluster

``` bash
az cloud list --output table
az cloud set --name AzureCloud
az account set --subscription 0e00d3c8-a691-4931-876e-7550b6c2eb1a
az aks get-credentials --resource-group RGKubernetes --name aks-for-data-services

kubectl get deployments --all-namespaces=true
```

# Deploy strizmi kafka and debezium connector

## Download packages
```bash
mkdir strimzi-debezium
cd strimzi-debezium

wget https://github.com/strimzi/strimzi-kafka-operator/releases/download/0.28.0/strimzi-0.28.0.tar.gz

wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-oracle/1.9.1.Final/debezium-connector-oracle-1.9.1.Final-plugin.tar.gz

wget https://repo1.maven.org/maven2/com/oracle/database/jdbc/ojdbc8/21.1.0.0/ojdbc8-21.1.0.0.jar

tar xvfz strimzi-0.28.0.tar.gz
tar xvfz debezium-connector-oracle-1.9.1.Final-plugin.tar.gz
mv ojdbc8-21.1.0.0.jar debezium-connector-oracle/
```

## Deploy strizmi kafka
### Deploy strizmi kafka operator
```shell
cd /root/strimzi-debezium/strimzi-0.28.0
sed -i 's/namespace: .*/namespace: ns4debezium/' install/cluster-operator/*RoleBinding*.yaml

kubectl create namespace ns4debezium
kubectl create -f /root/strimzi-debezium/strimzi-0.28.0/install/cluster-operator -n ns4debezium
kubectl get deployments -n ns4debezium
```

### Deploy strimzi kafka cluster and zookeeper cluster
```shell
vi /root/strimzi-debezium/strimzi-0.28.0/examples/kafka/kafka-persistent.yaml

kubectl apply -f /root/strimzi-debezium/strimzi-0.28.0/examples/kafka/kafka-persistent.yaml -n ns4debezium
kubectl get pods -n ns4debezium
```

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kaf-debez
spec:
  kafka:
    version: 3.1.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: external
        port: 9093
        type: nodeport
        tls: false
    config:
      auto.create.topics.enable: "true"
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.1"
    storage:
      type: jbod
      volumes:
      - id: 0
        class: azurefile-csi-premium
        type: persistent-claim
        size: 32Gi
        deleteClaim: false
      - id: 1
        class: azurefile-csi-premium
        type: persistent-claim
        size: 32Gi
        deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      class: azurefile-csi-premium
      type: persistent-claim
      size: 32Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

### Test kafka cluster

```shell
kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-console-producer.sh --broker-list kaf-debez-kafka-bootstrap:9092 --topic strimizi-demo-topic
-- input ---
{"ID":"1"}

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-console-consumer.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --topic strimizi-demo-topic --from-beginning
--- result ---
{"ID":"1"}

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-topics.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --list
--- result ---
Defaulted container "kafka" out of: kafka, kafka-init (init)
__consumer_offsets
__strimzi-topic-operator-kstreams-topic-store-changelog
__strimzi_store_topic
strimizi-demo-topic

kubectl get kafkatopic -n ns4debezium
kubectl -n ns4debezium delete kafkatopic <topic_name>
```

## Deploy debezium connector
### Build debezium connector w/ strimzi kafka connect image
```shell
cd /root/strimzi-debezium

cat <<EOF > Dockerfile
FROM quay.io/strimzi/kafka:0.28.0-kafka-3.1.0
USER root:root
RUN mkdir -p /opt/kafka/plugins/debezium
COPY ./debezium-connector-oracle/ /opt/kafka/plugins/debezium/
USER 1001
EOF

docker login acr4dataimages.azurecr.io
acr4dataimages
0D=7Xf3g8HCBLEcmY=Bqh7euSP5hcaHs

docker build . -t acr4dataimages.azurecr.io/connect-debezium-oracle
docker push acr4dataimages.azurecr.io/connect-debezium-oracle
```

### Configure oracle credentials to kubernetes
```shell
# Get base64 string
echo -n 'c##dbzuser' | base64
echo -n 'dbz' | base64
```

```bash
cat << EOF > oracle-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: debezium-secret-oracle
  namespace: ns4debezium
type: Opaque
data:
  orcluid: YyMjZGJ6dXNlcg==
  orclpwd: ZGJ6
EOF

kubectl apply -f oracle-credentials.yaml -n ns4debezium
```

```bash
cat << EOF > debezium-oracle-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: connector-configuration-oracle-role
  namespace: ns4debezium
rules:
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["debezium-secret-oracle"]
  verbs: ["get"]
EOF

kubectl apply -f debezium-oracle-role.yaml -n ns4debezium
```

```bash
cat << EOF > debezium-oracle-role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: connector-configuration-oracle-role-binding
  namespace: ns4debezium
subjects:
- kind: ServiceAccount
  name: oracle-connect-cluster-connect
  namespace: ns4debezium
roleRef:
  kind: Role
  name: connector-configuration-oracle-role
  apiGroup: rbac.authorization.k8s.io
EOF

kubectl apply -f debezium-oracle-role-binding.yaml -n ns4debezium
```

### Deploy debezium oracle kafka connect cluster
```bash
cat << EOF > debezium-oracle-connect.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnect
metadata:
  name: oracle-connect-cluster
  annotations:
    strimzi.io/use-connector-resources: "true"
spec:
  version: 3.1.0
  image: acr4dataimages.azurecr.io/connect-debezium-oracle:latest
  replicas: 1
  bootstrapServers: kaf-debez-kafka-bootstrap:9092
  config:
    config.providers: secrets
    config.providers.secrets.class: io.strimzi.kafka.KubernetesSecretConfigProvider
    group.id: connect-cluster
    offset.storage.topic: connect-cluster-offsets
    config.storage.topic: connect-cluster-configs
    status.storage.topic: connect-cluster-status
    auto.create.topics.enable: true
    config.storage.replication.factor: -1
    offset.storage.replication.factor: -1
    status.storage.replication.factor: -1
EOF

kubectl apply -f debezium-oracle-connect.yaml -n ns4debezium
```

### Deploy debezium oracle kafka connector configure
```bash
cat << EOF > oracle-connector.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: oracle-connector
  labels:
    strimzi.io/cluster: oracle-connect-cluster
spec:
  class: io.debezium.connector.oracle.OracleConnector
  tasksMax: 1
  config:
    tasks.max: 1
    connector.class: io.debezium.connector.oracle.OracleConnector
    database.hostname: 192.168.1.70
    database.port: 1521
    database.user: ${secrets:ns4debezium/debezium-secret-oracle:orcluid}
    database.password: ${secrets:ns4debezium/debezium-secret-oracle:orclpwd}
    database.server.name: oracle
    database.dbname: orclcdb
    database.pdb.name: orclpdb
    decimal.handling.mode: string
    database.history.kafka.bootstrap.servers: kaf-debez-kafka-bootstrap:9092
    database.history.kafka.topic: schema-changes.oracle
EOF

kubectl apply -f oracle-connector.yaml -n ns4debezium
```

### Check oracle debezium connector status

```bash
kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-topics.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --list

--- result ---
Defaulted container "kafka" out of: kafka, kafka-init (init)
__consumer_offsets
__strimzi-topic-operator-kstreams-topic-store-changelog
__strimzi_store_topic
connect-cluster-configs
connect-cluster-offsets
connect-cluster-status
oracle
oracle.C__DBZUSER.TAB001
schema-changes.oracle

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-console-consumer.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --topic oracle.C__DBZUSER.TAB001 --from-beginning

--- result ---
... show the latest message ...
{
    "schema": {
        "type": "struct",
        "fields": [
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": true,
                        "field": "ID"
                    }
                ],
                "optional": true,
                "name": "oracle.C__DBZUSER.TAB001.Value",
                "field": "before"
            },
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": true,
                        "field": "ID"
                    }
                ],
                "optional": true,
                "name": "oracle.C__DBZUSER.TAB001.Value",
                "field": "after"
            },
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": false,
                        "field": "version"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "connector"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "name"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "ts_ms"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "name": "io.debezium.data.Enum",
                        "version": 1,
                        "parameters": {
                            "allowed": "true,last,false,incremental"
                        },
                        "default": "false",
                        "field": "snapshot"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "db"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "sequence"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "schema"
                    },
                    {
                        "type": "string",
                        "optional": false,
                        "field": "table"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "txId"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "scn"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "commit_scn"
                    },
                    {
                        "type": "string",
                        "optional": true,
                        "field": "lcr_position"
                    }
                ],
                "optional": false,
                "name": "io.debezium.connector.oracle.Source",
                "field": "source"
            },
            {
                "type": "string",
                "optional": false,
                "field": "op"
            },
            {
                "type": "int64",
                "optional": true,
                "field": "ts_ms"
            },
            {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": false,
                        "field": "id"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "total_order"
                    },
                    {
                        "type": "int64",
                        "optional": false,
                        "field": "data_collection_order"
                    }
                ],
                "optional": true,
                "field": "transaction"
            }
        ],
        "optional": false,
        "name": "oracle.C__DBZUSER.TAB001.Envelope"
    },
    "payload": {
        "before": null,
        "after": {
            "ID": "1"
        },
        "source": {
            "version": "1.9.1.Final",
            "connector": "oracle",
            "name": "oracle",
            "ts_ms": 1657465073000,
            "snapshot": "false",
            "db": "ORCLPDB",
            "sequence": null,
            "schema": "C##DBZUSER",
            "table": "TAB001",
            "txId": "08000f0062020000",
            "scn": "2073675",
            "commit_scn": "2073775",
            "lcr_position": null
        },
        "op": "c",
        "ts_ms": 1657465078329,
        "transaction": null
    }
}
```

# Reference documents

> - https://strimzi.io/downloads/
> - https://strimzi.io/docs/operators/latest/full/deploying.html#cluster-operator-str
> - https://strimzi.io/docs/operators/in-development/configuring.html#assembly-accessing-kafka-outside-cluster-str
> - https://strimzi.io/blog/2020/01/27/deploying-debezium-with-kafkaconnector-resource/
> - https://dev.to/azure/kafka-on-kubernetes-the-strimzi-way-part-1-57g7
> - https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
> - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt
> - https://docs.docker.com/engine/install/ubuntu/
> - [Debezium Connector for Oracle :: Debezium Documentation](https://debezium.io/documentation/reference/stable/connectors/oracle.html)