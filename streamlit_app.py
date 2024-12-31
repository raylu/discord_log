import json

import pandas
import streamlit

@streamlit.cache_data
def load_data():
	with open('emoji_user_stats.json') as f:
		user_stats = json.load(f)
	users = user_stats['users']
	emojis = user_stats['emojis']
	return user_stats

streamlit.title('SHR emoji')
loading_text = streamlit.text('loading data...')
user_stats = load_data()
loading_text.empty()
if streamlit.checkbox('show raw user stats'):
	streamlit.json(user_stats)
