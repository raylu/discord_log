#!/usr/bin/env python3

import sys

import api_client

def main():
	client = api_client.APIClient()
	if len(sys.argv) == 1:
		guilds = client.request('/users/@me/guilds')
		for guild in guilds:
			print(guild['id'], guild['name'])
	else:
		(guild_id,) = sys.argv[1:]
		r = client.request('/users/@me/guilds/' + guild_id, 'DELETE')
		if r is not None:
			print(r)

if __name__ == '__main__':
	main()
