#!python3

import logging
import sys

from confluent_kafka import Consumer
from lab02_lib import Session, utf8_deserializer, session_deserializer

# Здесь реализуем BatchMessageConsumer
def main():
	
	# Среди требований есть запись ошибок в лог, значит надо настроить логирование
	logging.basicConfig(
		filename=f'{sys.argv[0]}.log',
		level=logging.INFO,
		format='%(asctime)s - %(levelname)s - %(message)s'
	)
	
	# Настройка консьюмера. DeserializingConsumer
	# конечно удобнее, но он не умеет в .consume, а умеет только в .poll,
	# а там судя по документации явно размер батча не пропишешь
	kafka_consumer_conf = {
    		'bootstrap.servers': '127.0.0.1:9094',
    		'group.id': 'lab02_group02',
    		'enable.auto.commit': False,
    		'auto.offset.reset': 'earliest',
    		'fetch.min.bytes': '460',
    		'fetch.wait.max.ms': '300000',
	}
	
	# Создание консьюмера
	consumer = Consumer(kafka_consumer_conf)

	# Подписка на топик
	consumer.subscribe(["lab02_topic"])

	# Чтение сообщений в бесконечном цикле
	try:
		while True:
			# Получение пакета сообщений
			messages = consumer.consume(num_messages=10, timeout=1000)
			if not messages:
				continue
			processed_cnt = 0
			for msg in messages:
				# При необходимости обрабатываем ошибку считывания
				if msg.error():
					if msg.error().code() == KafkaError._PARTITION_EOF:
 		                     		#Кончились сообщения в партиции
 			         		print(f"%% {msg.topic()} [{msg.partition()}] reached end offset {msg.offset()}")
					else:
						logging.error(msg.error())
						continue
				# Десериализуем сообщение, показываем его в стандартном выводе и при желании в логе
				key, value = utf8_deserializer(msg.key(), None), session_deserializer(msg.value(), None)
				processed_cnt += 1
				log_text = f"Message is received: key={key}, value={value}"
				print(log_text)
				logging.debug(log_text)
			if processed_cnt > 0:
				# Пишем, что пакет закончили обрабатывать
				consumer.commit(asynchronous=False)
				print(f'Number of records in batch: {processed_cnt}. Committed.')
	except KeyboardInterrupt:
		pass
	finally:
		# Закрытие консьюмера
		consumer.close()

if __name__ == "__main__":
	main()
