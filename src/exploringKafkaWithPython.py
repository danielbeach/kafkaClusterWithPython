import kafka


class PyKafka:
    def __init__(self, cluster_endpoints: list = []):
        self.endpoints = cluster_endpoints
        self.meta = None
        self.brokers = None
        self.topics = []
        self.meta_client = None
        self.client = None
        self.clientAdmin = None
        self.producer = None
        self.consumer = None

    def pull_cluster_meta(self):
        self.meta = kafka.cluster.ClusterMetadata(bootstrap_servers=self.endpoints,
                                                  request_timeout_ms=10000)

    def pull_broker_meta(self):
        self.brokers = self.meta.brokers()

    def pull_topics(self):
        self.topics.extend(list(self.meta.topics()))

    def set_meta_client(self, name: str = "default_meta"):
        self.meta_client = kafka.KafkaClient(bootstrap_servers=self.endpoints,
                                             client_id=name)

    def set_client_admin(self, name: str = "pyKafkaClient"):
        self.clientAdmin = kafka.KafkaAdminClient(bootstrap_servers=self.endpoints,
                                                  client_id=name,
                                                  request_timeout_ms=10000)

    def create_topics(self, topics_list: list = []) -> object:
        kr = self.clientAdmin.create_topics(topics_list)
        return kr

    def create_producer(self):
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.endpoints,
                                            client_id="pythonProducer",
                                            acks="all",
                                            retries=3)

    def send_message(self, topic: str,  message: bytes) -> object:
        future_record_meta = self.producer.send(topic=topic, value=message)
        return future_record_meta

    def get_producer_metrics(self):
        print(self.producer.metrics())

    def create_consumer(self):
        self.consumer = kafka.KafkaConsumer(bootstrap_servers=self.endpoints,
                                            client_id="pythonConsumer",
                                            auto_offset_reset="earliest")


if __name__ == '__main__':
    pK = PyKafka(cluster_endpoints=["198.58.124.54:9092", "173.255.199.161:9092", "50.116.17.69:9092"])
    pK.set_meta_client()
    pK.pull_cluster_meta()
    if pK.meta_client.bootstrap_connected():
        print("connected to meta client brokers")
        pK.pull_broker_meta()
        print(pK.brokers)
    pK.set_client_admin()
    topics_to_create = [kafka.admin.NewTopic(name="my_first_topic", num_partitions=1, replication_factor=2)]
    kafka_response = pK.create_topics(topics_list=topics_to_create)
    print(kafka_response)

    pK.create_producer()
    messages = [b'{"first_message": 1}', b'{"second_message": 2}']
    for message in messages:
        rmf = pK.send_message(topic="my_first_topic",
                              message=message)
        record_metadata = rmf.get(timeout=60)
        print(record_metadata)

    pK.create_consumer()
    pK.consumer.subscribe(["my_first_topic"])
    print(pK.consumer.subscription())
    records = pK.consumer.poll(max_records=10)
    for record in records:
        print(record)


