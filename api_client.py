import enum
import time

import requests

import config

class APIClient:
	def __init__(self):
		self.rs = requests.Session()
		self.rs.headers['Authorization'] = 'Bot ' + config.token
		self.rs.headers['User-Agent'] = 'DiscordBot (https://github.com/raylu/discord_log 0.0)'

	def request(self, path, method='GET', params=None):
		response = self.rs.request(method, 'https://discordapp.com/api' + path, params=params)
		response.raise_for_status()
		if response.headers.get('X-RateLimit-Remaining') == '0':
			time.sleep(int(response.headers['X-RateLimit-Reset-After']))
		if response.status_code != 204:
			return response.json()

	def get_channels(self):
		guilds = self.request('/users/@me/guilds')
		for guild in guilds:
			channels = self.request('/guilds/%s/channels' % guild['id'])
			for channel in channels:
				if channel['type'] != ChannelType.GUILD_TEXT:
					continue
				yield Channel(channel['id'], channel['name'], guild['id'], guild['name'])

	def get_messages(self, channel_id, after_id):
		while True:
			messages = self.request('/channels/%s/messages' % channel_id,
					params={'after': after_id, 'limit': 100})
			for message in reversed(messages): # messages come in reverse order
				yield message
			if len(messages) < 100:
				break
			after_id = messages[0]['id']

	def get_members(self, guild_id, after=None):
		return self.request('/guilds/%s/members' % guild_id, params={
			'limit': 1000,
			'after': after,
		})

	def kick(self, guild_id, user_id):
		self.request('/guilds/%s/members/%s' % (guild_id, user_id), method='DELETE')

class Channel:
	def __init__(self, channel_id, channel_name, guild_id, guild_name):
		self.id = channel_id
		self.name = channel_name
		self.guild_id = guild_id
		self.guild_name = guild_name

class ChannelType(enum.IntEnum):
	GUILD_TEXT = 0
