import enum
import time

import requests

import config

class APIClient:
	def __init__(self):
		self.rs = requests.Session()
		self.rs.headers['Authorization'] = 'Bot ' + config.token
		self.rs.headers['User-Agent'] = 'DiscordBot (https://github.com/raylu/discord_log 0.0)'

	def get(self, path, params=None):
		response = self.rs.get('https://discordapp.com/api' + path, params=params)
		response.raise_for_status()
		if response.headers['X-RateLimit-Remaining'] == '0':
			time.sleep(int(response.headers['X-RateLimit-Reset-After']))
		return response.json()

	def get_channels(self):
		guilds = self.get('/users/@me/guilds')
		for guild in guilds:
			channels = self.get('/guilds/%s/channels' % guild['id'])
			for channel in channels:
				if channel['type'] != ChannelType.GUILD_TEXT:
					continue
				yield Channel(channel['id'], channel['name'], guild['id'], guild['name'])

	def get_messages(self, channel_id, after_id):
		while True:
			messages = self.get('/channels/%s/messages' % channel_id,
					params={'after': after_id, 'limit': 100})
			for message in reversed(messages): # messages come in reverse order
				yield message
			if len(messages) < 100:
				break
			after_id = messages[0]['id']

	def get_members(self, guild_id, after=None):
		return self.get('/guilds/%s/members' % guild_id, params={
			'limit': 1000,
			'after': after,
		})

class Channel:
	def __init__(self, channel_id, channel_name, guild_id, guild_name):
		self.id = channel_id
		self.name = channel_name
		self.guild_id = guild_id
		self.guild_name = guild_name

class ChannelType(enum.IntEnum):
	GUILD_TEXT = 0
