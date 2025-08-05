#!python3

import sys
from confluent_kafka import SerializingProducer
from lab02_lib import Session, generate_random_time, generate_random_md5, Session, utf8_serializer, session_serializer

def main(msg_cnt):
	# Конфигурация продюсера – адрес сервера, сериализаторы, at least once
	conf = {
		'bootstrap.servers': '127.0.0.1:9094',
		'key.serializer': utf8_serializer,
		'value.serializer': session_serializer,
		'acks': 'all',
	}

	# Создание продюсера
	producer = SerializingProducer(conf)

	# Отправка сообщений
	# Сообщение - это объект класса Session c 2 полями - время начала сессии и ее md5-хэш
	for i in range(msg_cnt):
		session = Session(start=generate_random_time(), md5=generate_random_md5())
		print(session)
		producer.produce(topic="lab02_topic", key=f"key-{i}", value=session,)

	# Ожидание завершения отправки всех сообщений
	producer.flush()

if __name__ == '__main__':
	main(int(sys.argv[1]) if len(sys.argv) >= 2 else 10)
