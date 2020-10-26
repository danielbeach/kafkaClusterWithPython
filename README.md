## Setup a Kafka cluster - connect with Python ##

See full blog post here .... https://www.confessionsofadataguy.com/intro-to-apache-kafka-for-data-engineers/

# Setup a Kafka three node broker cluster.. with Zookeeper. #

- wget https://apache.claz.org/kafka/2.6.0/kafka_2.13-2.6.0.tgz
- tar -xzf kafka_2.13-2.6.0.tgz
- // lets add kafka location to path.
- vim ~/.bashrc
- // add the following line, then source ~/.bashrc
- export PATH=$PATH:$HOME/.local/bin:$HOME/bin:$HOME/kafka_2.13-2.6.0/bin

- cd ~/kafka_2.13-2.6.0/bin
- zookeeper-server-start.sh /home/beach/kafka_2.13-2.6.0/config/zookeeper.properties

- vim server.properties
- broker.id=0
- listeners=PLAINTEXT://0.0.0.0:9092
- advertised.listeners=PLAINTEXT://173.255.199.161:9092

- num.io.threads=4
- zookeeper.connect=173.255.199.161:2181

- kafka-server-start.sh /home/beach/kafka_2.13-2.6.0/config/server.properties

## src/exploringKafkaWithPython.py ##
A simple class to create a Topic, send messages via a Producer, and consume messages via a Consumer.





