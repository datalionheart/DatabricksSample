# Azure-Based MySQL CDC Open Source Solution

`debezium CDC connector for MySQL` 

`strimzi kafka cluster` `strizmi kafka zookeeper cluster` `strimzi kafka connect cluster`

`azure kubernetes services` `azure database for mysql` `azure databricks` `azure eventhub`

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

# List all deployments in all namespaces

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

wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-mysql/1.9.1.Final/debezium-connector-mysql-1.9.1.Final-plugin.tar.gz
wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/1.9.1.Final/debezium-connector-postgres-1.9.1.Final-plugin.tar.gz
wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-oracle/1.9.1.Final/debezium-connector-oracle-1.9.1.Final-plugin.tar.gz

tar xvfz strimzi-0.28.0.tar.gz
tar xvfz debezium-connector-mysql-1.9.1.Final-plugin.tar.gz
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

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-console-consumer.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --topic strimizi-demo-topic --from-beginning

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-topics.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --list
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

### Configure MySQL credentials to kubernetes
```shell
# Get base64 string
echo -n 'insadmin' | base64
echo -n '8F5F5071@5361@474a@8cc7@4E8299DFFBFE' | base64
```

```bash
cat << EOF > mysql-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: debezium-secret
  namespace: ns4debezium
type: Opaque
data:
  username: aW5zYWRtaW4=
  password: OEY1RjUwNzFANTM2MUA0NzRhQDhjYzdANEU4Mjk5REZGQkZF
EOF

kubectl apply -f mysql-credentials.yaml -n ns4debezium
```

```bash
cat << EOF > debezium-mysql-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: connector-configuration-role
  namespace: ns4debezium
rules:
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["debezium-secret"]
  verbs: ["get"]
EOF

kubectl apply -f debezium-mysql-role.yaml -n ns4debezium
```

```bash
cat << EOF > debezium-mysql-role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: connector-configuration-role-binding
  namespace: ns4debezium
subjects:
- kind: ServiceAccount
  name: mysql-connect-cluster-connect
  namespace: ns4debezium
roleRef:
  kind: Role
  name: connector-configuration-role
  apiGroup: rbac.authorization.k8s.io
EOF

kubectl apply -f debezium-mysql-role-binding.yaml -n ns4debezium
```

### Deploy debezium mysql kafka connect cluster
```bash
cat << EOF > debezium-mysql-connect.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnect
metadata:
  name: mysql-connect-cluster
  annotations:
    strimzi.io/use-connector-resources: "true"
spec:
  version: 3.1.0
  image: acr4dataimages.azurecr.io/connect-debezium:latest
  replicas: 1
  bootstrapServers: kaf-debez-kafka-bootstrap:9092
  config:
    config.providers: secrets
    config.providers.secrets.class: io.strimzi.kafka.KubernetesSecretConfigProvider
    group.id: connect-cluster
    offset.storage.topic: connect-cluster-offsets
    config.storage.topic: connect-cluster-configs
    status.storage.topic: connect-cluster-status
    # -1 means it will use the default replication factor configured in the broker
    auto.create.topics.enable: true
    config.storage.replication.factor: -1
    offset.storage.replication.factor: -1
    status.storage.replication.factor: -1
EOF

kubectl apply -f debezium-mysql-connect.yaml -n ns4debezium
```

### Deploy debezium mysql kafka connector configure
```bash
cat << EOF > classicmodels-connector.yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: classicmodels-connector
  labels:
    strimzi.io/cluster: mysql-connect-cluster
spec:
  class: io.debezium.connector.mysql.MySqlConnector
  tasksMax: 1
  config:
    tasks.max: 1
    connector.class: io.debezium.connector.mysql.MySqlConnector
    database.hostname: fsmy4debezium.mysql.database.azure.com
    database.port: 3306
    database.user: ${secrets:ns4debezium/debezium-secret:username}
    database.password: ${secrets:ns4debezium/debezium-secret:password}
    database.server.id: 184059
    database.server.name: fsmy4debezium.mysql.database.azure.com
    database.include.list: classicmodels
    table.include.list: "classicmodels.demo"
    database.history.kafka.bootstrap.servers: kaf-debez-kafka-bootstrap:9092
    database.history.kafka.topic: schema-changes.classicmodels
    include.schema.changes: true
EOF

kubectl apply -f classicmodels-connector.yaml -n ns4debezium
```

### Check mysql debezium connector status

```bash
kubectl -n ns4debezium get kctr classicmodels-connector -o yaml

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-topics.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --list

kubectl exec -n ns4debezium -i kaf-debez-kafka-0 -- bin/kafka-console-consumer.sh --bootstrap-server kaf-debez-kafka-bootstrap:9092 --topic fsmy4debezium.mysql.database.azure.com.classicmodels.orders --from-beginning
```

# Reference documents:

> - https://strimzi.io/downloads/
> - https://strimzi.io/docs/operators/latest/full/deploying.html#cluster-operator-str
> - https://strimzi.io/docs/operators/in-development/configuring.html#assembly-accessing-kafka-outside-cluster-str
> - https://strimzi.io/blog/2020/01/27/deploying-debezium-with-kafkaconnector-resource/
> - https://www.youtube.com/watch?v=TA_RhjfKm6Q
> - https://dev.to/azure/kafka-on-kubernetes-the-strimzi-way-part-1-57g7
> - https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
> - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt
> - https://docs.docker.com/engine/install/ubuntu/