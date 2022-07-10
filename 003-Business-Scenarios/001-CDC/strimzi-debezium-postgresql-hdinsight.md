# Azure-Based PostgreSQL CDC Open Source Solution

`debezium CDC connector for MySQL`  `strimzi kafka connect cluster` `azure hdinsight wo/ ESP`

`azure kubernetes services` `azure database for postgresql` `postgresql plugins: pgoutput`

# Objective

Debezium PostgreSQL Connector on Strimzi Kafka Connect Cluster Integration w/ Azure HDInsight wo/ ESP

[TOC]

# Architecture

![](./strimzi-debezium-hdinsight-picture/Debezium.png)

# Prepare HDInsight Kafka Cluster

![](./strimzi-debezium-hdinsight-picture/hdi001.png)

![](./strimzi-debezium-hdinsight-picture/hdi002.png)

> Parameter setting & Restart components:
>
> | Parameter Name             | Default Value | Set Value |
> | -------------------------- | ------------- | --------- |
> | auto.create.topics.enable  | false         | true      |
> | default.replication.factor | 4             | 3         |
> | num.replica.fetchers       | 4             | 3         |

![](./strimzi-debezium-hdinsight-picture/hdi003.png)

# Prepare azure database for postgresql

## Azure database for postgresql

![](./strimzi-debezium-pgsql-pictures/pgsql001.png)

## Set server parameters and restart server

| ID   | Parameter Item           | Value                     |
| ---- | ------------------------ | ------------------------- |
| 1    | wal_level                | LOGICAL                   |
| 2    | shared_preload_libraries | PGLOGICAL                 |
| 3    | azure.extensions         | PGLOGICAL                 |
| 4    | max_worker_processes     | 32 default 8, at least 16 |

## Publication Initial

```sql
ALTER ROLE insadmin WITH REPLICATION;
CREATE PUBLICATION PGPub FOR ALL TABLES;
SELECT pg_create_logical_replication_slot('pgoutput_slot', 'pgoutput');
```

> - [`decoderbufs`](https://github.com/debezium/postgres-decoderbufs) is based on Protobuf and maintained by the Debezium community.
> - [`wal2json`](https://github.com/eulerto/wal2json) is based on JSON and maintained by the wal2json community (deprecated, scheduled for removal in Debezium 2.0).
> - `pgoutput` is the standard logical decoding output plug-in in PostgreSQL 10+. It is maintained by the PostgreSQL community, and used by PostgreSQL itself for [logical replication](https://www.postgresql.org/docs/current/logical-replication-architecture.html). This plug-in is always present so no additional libraries need to be installed. The Debezium connector interprets the raw replication event stream directly into change events.

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

wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/1.9.1.Final/debezium-connector-postgres-1.9.1.Final-plugin.tar.gz

tar xvfz strimzi-0.28.0.tar.gz
tar xvfz debezium-connector-postgres-1.9.1.Final-plugin.tar.gz
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

## Deploy debezium connector
### Build debezium connector w/ strimzi kafka connect image
```shell
cd /root/strimzi-debezium

cat <<EOF > Dockerfile
FROM quay.io/strimzi/kafka:0.28.0-kafka-3.1.0
USER root:root
RUN mkdir -p /opt/kafka/plugins/debezium
COPY ./debezium-connector-mysql/ /opt/kafka/plugins/debezium/
USER 1001
EOF

docker login acr4dataimages.azurecr.io
acr4dataimages
0D=7Xf3g8HCBLEcmY=Bqh7euSP5hcaHs

docker build . -t acr4dataimages.azurecr.io/connect-debezium
docker push acr4dataimages.azurecr.io/connect-debezium
```

### Configure PostgreSQL credentials to kubernetes
```shell
# Get base64 string
echo -n 'insadmin' | base64
echo -n '8F5F5071@5361@474a@8cc7@4E8299DFFBFE' | base64
```

```bash
cat << EOF > postgres-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: debezium-secret-postgres
  namespace: ns4debezium
type: Opaque
data:
  pgsqluid: aW5zYWRtaW4=
  pgsqlpwd: OEY1RjUwNzFANTM2MUA0NzRhQDhjYzdANEU4Mjk5REZGQkZF
EOF

kubectl apply -f postgres-credentials.yaml -n ns4debezium
```

```bash
cat << EOF > debezium-postgres-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: connector-configuration-postgres-role
  namespace: ns4debezium
rules:
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["debezium-secret-postgres"]
  verbs: ["get"]
EOF

kubectl apply -f debezium-postgres-role.yaml -n ns4debezium
```

```bash
cat << EOF > debezium-postgres-role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: connector-configuration-postgres-role-binding
  namespace: ns4debezium
subjects:
- kind: ServiceAccount
  name: postgres-connect-cluster-connect
  namespace: ns4debezium
roleRef:
  kind: Role
  name: connector-configuration-postgres-role
  apiGroup: rbac.authorization.k8s.io
EOF

kubectl apply -f debezium-postgres-role-binding.yaml -n ns4debezium
```

### Deploy debezium postgresql kafka connect cluster
```bash
cat << EOF > debezium-postgres-connect.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnect
metadata:
  name: postgres-connect-cluster
  annotations:
    strimzi.io/use-connector-resources: "true"
spec:
  version: 3.1.0
  image: acr4dataimages.azurecr.io/connect-debezium-postgres:latest
  replicas: 1
  bootstrapServers: "192.168.2.75:9092,192.168.2.73:9092,192.168.2.74:9092"
  config:
    config.providers: secrets
    config.providers.secrets.class: io.strimzi.kafka.KubernetesSecretConfigProvider
    group.id: connect-cluster-group
    offset.storage.topic: connect-cluster-offsets
    config.storage.topic: connect-cluster-configs
    status.storage.topic: connect-cluster-status
    auto.create.topics.enable: true
    offset.flush.interval.ms: 10000
    rest.advertised.host.name: connect
    key.converter: org.apache.kafka.connect.json.JsonConverter
    value.converter: org.apache.kafka.connect.json.JsonConverter
    key.converter.schemas.enable: false
    value.converter.schemas.enable: false
    internal.key.converter.schemas.enable: false
    internal.value.converter.schemas.enable: false
    internal.key.converter: org.apache.kafka.connect.json.JsonConverter
    internal.value.converter: org.apache.kafka.connect.json.JsonConverter
    config.storage.replication.factor: 3
    offset.storage.replication.factor: 3
    status.storage.replication.factor: 3
    producer.connections.max.idle.ms: 180000
    producer.metadata.max.age.ms: 180000
EOF

kubectl apply -f debezium-postgres-connect.yaml -n ns4debezium
```

### Deploy debezium postgresql kafka connector configure
```bash
cat << EOF > dvdrental-connector.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: dvdrental-connector
  labels:
    strimzi.io/cluster: postgres-connect-cluster
spec:
  class: io.debezium.connector.postgresql.PostgresConnector
  tasksMax: 1
  config:
    tasks.max: 1
    connector.class: io.debezium.connector.postgresql.PostgresConnector
    database.hostname: fspgsql4dbz.postgres.database.azure.com
    database.port: 5432
    database.user: ${secrets:ns4debezium/debezium-secret-postgres:pgsqluid}
    database.password: ${secrets:ns4debezium/debezium-secret-postgres:pgsqlpwd}
    database.server.id: 184080
    database.server.name: fspgsql4dbz
    database.dbname: dvdrental
    database.history.kafka.bootstrap.servers: "192.168.2.75:9092,192.168.2.73:9092,192.168.2.74:9092"
    database.history.kafka.topic: schema-changes.dvdrental
    include.schema.changes: true
    plugin.name: "pgoutput"
    publication.name: "pgpub"
    publication.autocreate.mode: "filtered"
    slot.name: "pgoutput_slot"
EOF

kubectl apply -f dvdrental-connector.yaml -n ns4debezium
```

### Check CDC Topic Status

#### Check Topic List

```bash
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --list --zookeeper 192.168.2.71:2181,192.168.2.69:2181,192.168.2.70:2181

--- Result ---
__consumer_offsets
connect-cluster-configs
connect-cluster-offsets
connect-cluster-status
fspgsql4dbz.public.actor
fspgsql4dbz.public.address
fspgsql4dbz.public.category
fspgsql4dbz.public.city
fspgsql4dbz.public.country
fspgsql4dbz.public.customer
fspgsql4dbz.public.film
fspgsql4dbz.public.film_actor
fspgsql4dbz.public.film_category
fspgsql4dbz.public.inventory
fspgsql4dbz.public.language
fspgsql4dbz.public.payment
fspgsql4dbz.public.rental
fspgsql4dbz.public.staff
fspgsql4dbz.public.store
```

#### Check Topic Status

```bash
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper 192.168.2.71:2181,192.168.2.69:2181,192.168.2.70:2181 --describe --topic fspgsql4dbz.public.customer

--- Result ---
Topic:fspgsql4dbz.public.customer       PartitionCount:1        ReplicationFactor:3     Configs:
        Topic: fspgsql4dbz.public.customer      Partition: 0    Leader: 1001    Replicas: 1001,1003,1002        Isr: 1001,1003,1002
```

#### Check Topic Content

```bash
/usr/hdp/current/kafka-broker/bin/kafka-console-consumer.sh --bootstrap-server 192.168.2.75:9092,192.168.2.73:9092,192.168.2.74:9092 --topic fspgsql4dbz.public.customer --from-beginning

--- Result ---
... show the latest message ...
{"before":null,"after":{"customer_id":524,"store_id":1,"first_name":"Jacky003","last_name":"Ely","email":"jared.ely@sakilacustomer.org","address_id":530,"activebool":true,"create_date":13193,"last_update":1657377371300596,"active":1},"source":{"version":"1.9.1.Final","connector":"postgresql","name":"fspgsql4dbz","ts_ms":1657377371300,"snapshot":"false","db":"dvdrental","sequence":"[null,\"889218744\"]","schema":"public","table":"customer","txId":6133,"lsn":889218744,"xmin":null},"op":"u","ts_ms":1657427216008,"transaction":null}
^CProcessed a total of 600 messages
```


# Reference documents

> [Quickstart: Set up Apache Kafka on HDInsight using Azure portal | Microsoft Docs](https://docs.microsoft.com/en-us/azure/hdinsight/kafka/apache-kafka-get-started)
