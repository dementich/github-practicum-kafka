#!python3

import json
import random
import time
import argparse
from confluent_kafka import SerializingProducer
from lib import serialize_to_utf8, generate_random_sentence
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--topic', type=str)
parser.add_argument('-mc', '--message_count', type=int)

conf_text = {	'bootstrap.servers': 'localhost:9094,localhost:9095,localhost:9096',
		'key.serializer': serialize_to_utf8,
		'value.serializer': serialize_to_utf8,
		'acks': 'all',
		'enable.idempotence': True,
}

def handle_delivery(err, msg):
	if err is not None:
		print(f'Message delivery failed: {err}')
	else:
		print(f'Message delivered to {msg.topic()} topic [{msg.partition()}] @ offset {msg.offset()}')

def produce_messages(topic, message_count):
	producer = SerializingProducer(conf_text)
	for i in range(message_count):
		producer.produce(topic=topic, key=f'{i}', value=generate_random_sentence(), on_delivery=handle_delivery)
		if (i + 1) % 10_000 == 0:
			producer.flush()
		#time.sleep(random.randint(1, 5))
	producer.flush()

def main():
	args = parser.parse_args()
	produce_messages(args.topic, args.message_count)

if __name__ == "__main__":
	main()
