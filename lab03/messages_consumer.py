#!python3

import faust
import json
from confluent_kafka import SerializingProducer
from lab03_lib import User, deserialize_from_utf8, deserialize_from_utf8_json

#app = faust.App("lab03", broker="kafka://127.0.0.1:9094", store="rocksdb://", topic_partition=8)
app = faust.App("lab03", broker="kafka://127.0.0.1:9094", store="memory://", topic_partition=8)
tbl_blocked_users = app.Table('tbl_blocked_users', default=str)
tbl_censored_words = app.Table('tbl_censored_words', default=str)
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
		if await to_be_reset(words):
			await reset_tbl(tbl_censored_words)
			return
		tbl_censored_words['censored_words'] = words

async def to_be_reset(msg):
	return msg == '[]'

async def reset_tbl(tbl):
	async for key in tbl.keys():
		del tbl[key]

async def process_censored_words(data):
	result = data
	for censored_word in tbl_censored_words['censored_words']:
		result = result.replace(censored_word, '!!!CENSORED!!!')
	return result
	
@app.agent(tpc_messages)
async def process_messages(stream):
	i = 0
	async for msg_data in stream:
		msg_data['payload'] = await process_censored_words(msg_data['payload'])
		sender, receiver = msg_data['sender'], msg_data['receiver']
		if sender in tbl_blocked_users[receiver]:
			print(f'{sender} found in the black list of {receiver}')
		else:
			#print(f'receiver is not found in the black list...')
			await tpc_filtered_messages.send(key=f'key-{i}', value=msg_data)
		i += 1

if __name__ == "__main__":
	app.main()
