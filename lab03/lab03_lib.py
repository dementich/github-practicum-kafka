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

def generate_random_sentence():
	nouns = ["cat", "dog", "bird", "tree", "river", "car"]
	verbs = ["runs", "jumps", "sings", "flows", "drives", "sleeps"]
	adjectives = ["happy", "fast", "blue", "old", "shiny", "quiet"]
	adverbs = ["quickly", "loudly", "silently", "smoothly", "gracefully", "happily"]

	noun = random.choice(nouns)
	verb = random.choice(verbs)
	adjective = random.choice(adjectives)
	adverb = random.choice(adverbs)

	sentence = f"The {adjective} {noun} {verb} {adverb}."
	return sentence

def serialize_to_json_utf8(data, ctx=None):
	return json.dumps({'name': data.name, 'black_list': data.black_list}).encode('utf-8')

def serialize_to_utf8(data, ctx=None):
	return data.encode('utf-8')

def deserialize_from_utf8_json(data, ctx=None):
	return User.parse(json.loads(data.decode('utf-8')))

def deserialize_from_utf8(data, ctx=None):
	return data.decode('utf-8')
