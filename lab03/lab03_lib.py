#!python3

import json
import random

class User:
	def __init__(self, name, black_list):
		self.name = name
		self.black_list = black_list

	def __repr__(self):
		return str(self)

	def __str__(self):
		return f'User(name={self.name}, black_list={self.black_list})'

	@classmethod
	def parse(cls, src):
		return cls(src['name'], src['black_list'])

def load_json(file_name):
	try:
		with open(file_name, 'r') as src_file:
                	return json.load(src_file)
	except FileNotFoundError:
        	print(f'Error: "{file_name}" not found.')
	except json.JSONDecodeError:
		print(f'Error: Invalid JSON format in "{file_name}"')

def load_users(file_name):
	return [User.parse(raw_item) for raw_item in load_json(file_name)]

def generate_random_sentence():
	nouns = ["cat", "dog", "bird", "tree", "river", "car"]
	verbs = ["runs", "jumps", "sings", "flows", "drives", "sleeps"]
	adjectives = ["happy", "fast", "blue", "old", "shiny", "quiet"]
	adverbs = ["quickly", "loudly", "silently", "smoothly", "gracefully", "happily"]
	censored_words = [word for word in load_json('censored_words.json')]

	noun = random.choice(nouns)
	verb = random.choice(verbs)
	adjective = random.choice(adjectives)
	adverb = random.choice(adverbs)
	censored_word = random.choice(censored_words)

	sentence = f"The {adjective} {noun} {verb} {adverb}. The {censored_word}!"
	return sentence

def serialize_to_json_utf8(data, ctx=None):
	return json.dumps({'name': data.name, 'black_list': data.black_list}).encode('utf-8')

def serialize_to_utf8(data, ctx=None):
	return data.encode('utf-8')

def deserialize_from_utf8_json(data, ctx=None):
	return User.parse(json.loads(data.decode('utf-8')))

def deserialize_from_utf8(data, ctx=None):
	return data.decode('utf-8')
