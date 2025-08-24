#!python3

import json
import random

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

def serialize_to_utf8(data, ctx=None):
	return data.encode('utf-8')

def deserialize_from_utf8(data, ctx=None):
	return data.decode('utf-8')
