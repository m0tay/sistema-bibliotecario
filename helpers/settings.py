import json
import os

SETTINGS_FILE = 'settings.json'
DEFAULT_SETTINGS = {'width': 30, 'page_size': 10}


def setup():
	if not os.path.exists(SETTINGS_FILE):
		with open(SETTINGS_FILE, 'w') as file:
			json.dump(DEFAULT_SETTINGS, file)
		return DEFAULT_SETTINGS

	with open(SETTINGS_FILE) as file:
		settings = json.load(file)
	return settings


def update(new_settings):
	settings = setup()
	settings.update(new_settings)

	with open(SETTINGS_FILE, 'w') as file:
		json.dump(settings, file)

	return settings
