#!python3

import json
import random
import time
import faust
import argparse
from confluent_kafka import SerializingProducer
from lab03_lib import User, serialize_to_utf8, serialize_to_json_utf8, generate_random_sentence, load_json, load_users
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--black_list', action='store_true')
parser.add_argument('--censored_words', type=str)
parser.add_argument('--message_count', type=int)

conf_text = {	'bootstrap.servers': '127.0.0.1:9094',
		'key.serializer': serialize_to_utf8,
		'value.serializer': serialize_to_utf8,
		'acks': 'all',
}

conf_json = {	'bootstrap.servers': '127.0.0.1:9094',
		'key.serializer': serialize_to_utf8,
		'value.serializer': serialize_to_json_utf8,
		'acks': 'all',
}

def produce_black_list():
	users = load_users('./users.json')
	producer = SerializingProducer(conf_json)
	for user in users:
		producer.produce(topic='blocked_users', key=user.name, value=user)
	producer.flush()

def produce_censored_words(file):
	censored_words = [word for word in load_json(file)]
	producer = SerializingProducer(conf_text)
	producer.produce(topic='censored_words', key='word_list', value=json.dumps(censored_words))
	producer.flush()

def produce_messages(message_count):
	users = load_users('./users.json')
	producer = SerializingProducer(conf_text)
	for i in range(message_count):
		sender, receiver, payload = random.choice(users).name, random.choice(users).name, generate_random_sentence()
		msg_header = f'key={sender}'
		msg_val = {'sender': sender, 'receiver': receiver, 'payload': payload}
		producer.produce(topic='messages', key=msg_header, value=json.dumps(msg_val))
		if (i + 1) % 50_000 == 0:
			producer.flush()
		time.sleep(random.randint(1, 5))

def main():
	args = parser.parse_args()
	if args.black_list:
		produce_black_list()
	if args.censored_words:
		produce_censored_words(args.censored_words)
	if args.message_count and args.message_count > 0:
		produce_messages(args.message_count)

if __name__ == "__main__":
	main()
