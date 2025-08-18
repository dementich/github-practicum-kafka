#!python3

import faust
import json
from confluent_kafka import SerializingProducer
from lab03_lib import User, deserialize_from_utf8, deserialize_from_utf8_json

app = faust.App("lab03", broker="kafka://127.0.0.1:9094", store="rocksdb://", topic_partition=3)
tbl_blocked_users = app.GlobalTable('tbl_blocked_users', default=str)
tbl_censored_words = app.GlobalTable('tbl_censored_words', default=str)
tpc_blocked_users = app.topic('blocked_users')
tpc_censored_words = app.topic('censored_words')
tpc_messages = app.topic('messages')
tpc_filtered_messages = app.topic('filtered_messages')

@app.agent(tpc_blocked_users)
async def process_blocked_users(stream):
	async for user_data in stream:
		user = User.parse(user_data)
		tbl_blocked_users[user.name] = user.black_list

@app.agent(tpc_censored_words)
async def process_censored_words(stream):
	async for words in stream:
		if words == '[]':
			del tbl_censored_words['censored_words']
		else:
			tbl_censored_words['censored_words'] = words

def process_censored_words(data):
	result = data
	for censored_word in tbl_censored_words['censored_words']:
		result = result.replace(censored_word, '!!!CENSORED!!!')
	return result
	
@app.agent(tpc_messages)
async def process_messages(stream):
	async for msg_data in stream:
		msg_data['payload'] = process_censored_words(msg_data['payload'])
		sender, receiver = msg_data['sender'], msg_data['receiver']
		if sender in tbl_blocked_users[receiver]:
			print(f'{sender} found in the black list of {receiver}')
		else:
			await tpc_filtered_messages.send(key=f'key-{sender}', value=msg_data)

if __name__ == "__main__":
	app.main()
