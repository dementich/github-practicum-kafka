#!python3

import sys
import datetime
import random
import string
import hashlib
import secrets

def generate_random_time():
	return datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))

def generate_random_md5():
	"""Generates a random MD5 hash string."""
	# 1. Генерируем строку, от которой возьмем MD5
	random_input_length = 32
	characters = string.ascii_letters + string.digits + string.punctuation
	random_string = ''.join(secrets.choice(characters) for i in range(random_input_length))

	# 2. Сериализуем эту строку в массив байт
	encoded_string = random_string.encode('utf-8')

	# 3. Берем от этого массива байт MD5-хэш
	md5_hash = hashlib.md5(encoded_string)

	# 4. Берем шестнадцатиричное представление этого хеша
	return md5_hash.hexdigest()

class Session:
	def __init__(self, start, md5):
		self.start = start
		self.md5 = md5

	def __str__(self):
		return f'Session start time = {self.start}, session md5 hash = {self.md5}'

# Прописываем все необходимые нам сериализаторы/десериализаторы

def utf8_serializer(data, ctx):
	return data.encode('utf-8')

def utf8_deserializer(data, ctx):
	return data.decode('utf-8')

def session_serializer(session, ctx):
	result = str(session.start).encode('utf-8')
	result += session.md5.encode('utf-8')
	return result

def session_deserializer(data, ctx):
	start = datetime.datetime.strptime(data[0:8].decode('utf-8'), '%H:%M:%S').time()
	md5 = data[8:].decode('utf-8')
	return Session(start, md5)

# А здесь просто тестируем корректность сериализации/десериализации
if __name__ == '__main__':
	for i in range(int(sys.argv[1]) if len(sys.argv) >= 2 else 10):
		session = Session(start=generate_random_time(), md5=generate_random_md5())
		print(session)
		print(deserialize(serialize(session)))

