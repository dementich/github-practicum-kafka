#!zsh
ID=$(docker ps --no-trunc -aqf "name=lab03-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic blocked_users --bootstrap-server 127.0.0.1:9092 --partitions 3 --replication-factor 3
ID=$(docker ps --no-trunc -aqf "name=lab03-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic censored_words --bootstrap-server 127.0.0.1:9092 --partitions 3 --replication-factor 3
ID=$(docker ps --no-trunc -aqf "name=lab03-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic messages --bootstrap-server 127.0.0.1:9092 --partitions 3 --replication-factor 3
ID=$(docker ps --no-trunc -aqf "name=lab03-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic filtered_messages --bootstrap-server 127.0.0.1:9092 --partitions 3 --replication-factor 3
ID=$(docker ps --no-trunc -aqf "name=lab03-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic lab03-tbl_blocked_users-changelog --bootstrap-server 127.0.0.1:9092 --partitions 3 --replication-factor 3
ID=$(docker ps --no-trunc -aqf "name=lab03-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic lab03-tbl_censored_words-changelog --bootstrap-server 127.0.0.1:9092 --partitions 3 --replication-factor 3
