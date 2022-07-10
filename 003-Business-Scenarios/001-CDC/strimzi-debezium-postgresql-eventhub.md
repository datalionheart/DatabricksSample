# Azure-Based PostgreSQL CDC Open Source Solution

`debezium CDC connector for postgresql`  `strimzi kafka connect cluster` `azure eventhub`

`azure kubernetes services` `azure database for postgresql` `postgresql plugins: pgoutput`

# Objective

Debezium PostgreSQL Connector on Strimzi Kafka Connect Cluster Integration w/ Azure Event Hub

> Suggest: CDC Production Environment require Azure Event Hub at least the Premium pricing tier

[TOC]

# Architecture

![](./strimzi-debezium-hdinsight-picture/Debezium.png)

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

wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-mysql/1.9.1.Final/debezium-connector-postgres-1.9.1.Final-plugin.tar.gz

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
COPY ./debezium-connector-postgres/ /opt/kafka/plugins/debezium/
USER 1001
EOF

docker login acr4dataimages.azurecr.io
acr4dataimages
0D=7Xf3g8HCBLEcmY=Bqh7euSP5hcaHs

docker build . -t acr4dataimages.azurecr.io/connect-debezium-postgres
docker push acr4dataimages.azurecr.io/connect-debezium-postgres
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
cat << EOF > eventhub-postgres-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: eventhub-postgres-secret
type: Opaque
stringData:
  eventhubspassword: Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=3BdY8wvKw90qoubLkJKttCe/MNUt8AWgY6OkgDWm1w0=
EOF

kubectl apply -f eventhub-postgres-credentials.yaml -n ns4debezium
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
  resourceNames: ["debezium-secret-postgres", "eventhub-postgres-secret"]
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
  bootstrapServers: ehdebezcdc.servicebus.windows.net:9093
  config:
    config.providers: secrets
    config.providers.secrets.class: io.strimzi.kafka.KubernetesSecretConfigProvider
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
    config.storage.replication.factor: 1
    offset.storage.replication.factor: 1
    status.storage.replication.factor: 1
    producer.connections.max.idle.ms: 180000
    producer.metadata.max.age.ms: 180000
  authentication:
    type: plain
    username: $ConnectionString
    passwordSecret:
      secretName: eventhub-postgres-secret
      password: eventhubspassword
  tls:
    trustedCertificates: []
EOF

kubectl apply -f debezium-postgres-connect.yaml -n ns4debezium
```

### Deploy debezium postgresql kafka connector configure
```bash
cat << EOF > dvdrental-postgres-eventhub-connector.yaml
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
    database.allowPublicKeyRetrieval: true
    database.user: ${secrets:ns4debezium/debezium-secret-postgres:pgsqluid}
    database.password: ${secrets:ns4debezium/debezium-secret-postgres:pgsqlpwd}
    database.server.id: 184085
    database.server.name: fspgsql4dbz
    database.dbname: dvdrental
    auto.create.topics.enable: true
    database.history: io.debezium.relational.history.MemoryDatabaseHistory
    database.history.kafka.topic: dbhistory.dvdrental
    include.schema.changes: true
    plugin.name: "pgoutput"
    publication.name: "pgpub"
    publication.autocreate.mode: "filtered"
    slot.name: "pgoutput_slot"
    database.history.kafka.bootstrap.servers: ehdebezcdc.servicebus.windows.net:9093
    database.history.security.protocol: SASL_SSL
    database.history.sasl.mechanism: PLAIN
    database.history.sasl.jaas.config: "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=Consumer;SharedAccessKey=DCof4hGWLIq6vFRccfsvjTyDvwMDjEDgSvYvRTs2Vl0=\";"
    database.history.consumer.bootstrap.servers: ehdebezcdc.servicebus.windows.net:9093
    database.history.consumer.security.protocol: SASL_SSL
    database.history.consumer.sasl.mechanism: PLAIN
    database.history.consumer.sasl.jaas.config: "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=Consumer;SharedAccessKey=DCof4hGWLIq6vFRccfsvjTyDvwMDjEDgSvYvRTs2Vl0=\";"
    database.history.producer.bootstrap.servers: ehdebezcdc.servicebus.windows.net:9093
    database.history.producer.security.protocol: SASL_SSL
    database.history.producer.sasl.mechanism: PLAIN
    database.history.producer.sasl.jaas.config: "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"$ConnectionString\" password=\"Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=Consumer;SharedAccessKey=DCof4hGWLIq6vFRccfsvjTyDvwMDjEDgSvYvRTs2Vl0=\";"
EOF

kubectl apply -f dvdrental-postgres-eventhub-connector.yaml -n ns4debezium
```

### Check CDC Topic Status

![](./strimzi-debezium-eventhub-picture/status001-pgsql.png)

![](./strimzi-debezium-eventhub-picture/status002-pgsql.png)

![](./strimzi-debezium-eventhub-picture/status003-pgsql.png)

![](./strimzi-debezium-eventhub-picture/status004-pgsql.png)


# Reference documents

> - [Azure Event Hubs quotas and limits]([Quotas and limits - Azure Event Hubs - Azure Event Hubs | Microsoft Docs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas))

| Limit                                 | Basic                           | Standard                       | Premium                              | Dedicated                          |
| ------------------------------------- | ------------------------------- | ------------------------------ | ------------------------------------ | ---------------------------------- |
| Number of namespaces per subscription | 1000                            | 1000                           | 1000                                 | 1000 (50 per CU)                   |
| Number of event hubs per namespace    | 10                              | 10                             | 100 per PU                           | 1000                               |
| Capacity                              | $0.015/hour per Throughput Unit | $0.03/hour per Throughput Unit | $1.336/hour per Processing Unit (PU) | $8.001/hour per Capacity Unit (CU) |
| Ingress events                        | $0.028 per million events       | $0.028 per million events      | Included                             | Included                           |
| Apache Kafka                          |                                 | √                              | √                                    | √                                  |
| Schema Registry                       |                                 | √                              | √                                    | √                                  |
| Max Retention Period                  | 1 day                           | 7 days                         | 90 days                              | 90 days                            |