import configparser
import json
from re import search
import channel_list
import parsingPage
import find_items
import asyncio
import text
from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)
client.start()


def dump_all_messages(channel):
	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 100   # максимальное число записей, передаваемых за один раз

	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

	class DateTimeEncoder(json.JSONEncoder):
		'''Класс для сериализации записи дат в JSON'''
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		 json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


# def main(url):
# 	# url = input("Введите ссылку на канал или чат: ")
# 	channel = client.get_entity(url)
# 	dump_all_messages(channel)


# def client_start(item):

# 	posts = []
# 	for url in channel_list.channel_list:
# 		try:
# 			channel = client.get_entity(url)
# 			dump_all_messages(channel)
# 			posts += find_items.find_item(parsingPage.making_list("channel_messages.json",url),item)
# 		except:
# 			pass

# 	return posts
def making_big_list():
	all_posts =[]
	num_post = 0
	num_eror = 0
	for url in channel_list.channel_list:
		try:
			dump_all_messages(url)
			all_posts += parsingPage.making_list("channel_messages.json",url)
			num_post += 1
		except:
			num_eror += 1
			pass
	print(f'Спарсил {num_post} каналов. Поймал ошибок: {num_eror}')
	return all_posts

	
def search_engine(file,item):
	posts = []
	posts += find_items.find_item(file,item)
	if posts:
		return posts
	else:
		return(text.nothing_in_list)


a = making_big_list()
# print(client_start('Dior'))
