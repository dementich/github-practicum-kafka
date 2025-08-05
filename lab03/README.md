# Как воспроизвести работу:

1.	Поднимаем кластер с kafka зайдя в каталог с файлом docker-compose.yaml и запустив команду docker compose -f docker-compose.yaml up -d. Ему надо, чтобы были свободны порты 9094, 9095, 9096 и 8080.

2.	Идем в браузере на 127.0.0.1:8080. Там должен отображаться пользовательский интерфейс kafka-ui и должно быть видно, что у нас 3 брокера

3.	Создаем топик lab02_topic выполнив в командной строке 
```bash
ID=$(docker ps --no-trunc -aqf "name=kafka-cluster-app-kafka-0-1") && docker exec -it $ID /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic lab02_topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 2
```

4.	Предполагается, что все действия код выполняет в рамках определенного окружения на основе Python 3.12.4. Можно как попробовать поставить свое окружение, так и скачать ровно то, на котором тестировал (
https://disk.yandex.ru/d/xP3uTDMbgUtPEg). Перед выполнением кода окружение надо активировать: source ./env/bin/activate. Потом деактивировать его можно командой deactivate.

5.	Запускаем SingleMessageConsumer командой ./lab02_consumer01.py и BatchMessageConsumer командой ./lab02_consumer02.py

6.	Отправляем в топик например 100 сообщений командой ./lab02_producer.py 100 (предварительно не забываем активировать окружение) и смотрим на то, что вывели консьюмеры.
