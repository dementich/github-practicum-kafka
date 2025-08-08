#!python3

import json
import random
import time
from confluent_kafka import SerializingProducer
from lab03_lib import User, serialize_to_utf8, generate_random_sentence
from datetime import datetime

def load_users(file_name):
	try:
		with open(file_name, 'r') as src_file:
			return json.load(src_file)
	except FileNotFoundError:
		print(f'Error: "{file_name}" not found.')
	except json.JSONDecodeError:
		print(f'Error: Invalid JSON format in "{file_name}"')

def main():
	conf = {'bootstrap.servers': '127.0.0.1:9094',
		'key.serializer': serialize_to_utf8,
		'value.serializer': serialize_to_utf8,
		'acks': 'all',
	}
	users = [User.parse(raw_data) for raw_data in load_users('./users.json')]
	producer = SerializingProducer(conf)
	for i in range(100):
		msg_header = f'{datetime.now().time()} - {random.choice(users).name}'
		msg_text = generate_random_sentence()
		producer.produce(topic='lab03_topic', key=msg_header, value=msg_text)
		if (i + 1) % 50_000 == 0:
			producer.flush()
		time.sleep(random.randint(1, 5))

if __name__ == "__main__":
	main()
