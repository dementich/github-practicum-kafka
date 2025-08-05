#!python3

import logging
import sys

from confluent_kafka import DeserializingConsumer
from lab02_lib import Session, utf8_deserializer, session_deserializer

# Здесь реализуем SingleMessageConsumer
def main():
	# Среди требований есть запись ошибок в лог, значит надо настроить логирование	
	logging.basicConfig(
		filename=f'{sys.argv[0]}.log',
		level=logging.INFO,
		format='%(asctime)s - %(levelname)s - %(message)s'
	)
	
	# Настраиваем DeserializingConsumer
	kafka_consumer_conf = {
    		'bootstrap.servers': '127.0.0.1:9094',
    		'group.id': 'lab02_group01',
    		'auto.offset.reset': 'earliest',
    		'key.deserializer': utf8_deserializer,
    		'value.deserializer': session_deserializer,
	}
	
	# Создание консьюмера
	consumer = DeserializingConsumer(kafka_consumer_conf)

	# Подписка на топик
	consumer.subscribe(["lab02_topic"])

	# Чтение сообщений в бесконечном цикле
	try:
		while True:
			# Получение сообщения
			msg = consumer.poll(0.5)
			if msg is None:
				continue
			if msg.error():
				logging.error(msg.error())
				continue
			# Генерируем текст для лога и пишем его при необходимости в лог и на экран
			log_text = f"Message is received: key={msg.key()}, value={msg.value()}, offset={msg.offset()}"
			print(log_text)
			logging.debug(log_text)
	except KeyboardInterrupt:
		pass
	finally:
    		# Закрытие консьюмера
   	 consumer.close()

if __name__ == "__main__":
	main()
