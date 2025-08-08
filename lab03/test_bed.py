#!python3

import json

def loadUsers(fileName):
	try:
		with open(fileName, 'r') as srcFile:
			return json.load(srcFile)
	except FileNotFoundError:
		print(f'Error: "{fileName}" not found.')
	except json.JSONDecodeError:
		print(f'Error: Invalid JSON format in "{fileName}"')

def main():
	print(loadUsers('./users.json'))

if __name__ == '__main__':
	main()
