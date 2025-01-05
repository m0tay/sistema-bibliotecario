from datetime import date
from os import name, system
from typing import Dict

SETTINGS: Dict


def setup(settings: dict):
	# se não criar, atualiza
	global SETTINGS
	SETTINGS = settings


def clear_cli():
	return system('cls') if name == 'nt' else system('clear')


def in_range(index: int, browse_range: Dict[str, int]) -> bool:
	return browse_range['start'] <= index < browse_range['end']


def menu(options: Dict[str, str], pages=None):
	global SETTINGS
	if pages:
		print(
			f"{' ' + f'Page: {pages['at']}/{pages['total']} ({SETTINGS['page_size']} per page)' + ' ':-^{SETTINGS['width']}}"
		)
	print(f"{' ' + date.today().strftime('%A %d, %B %Y') + ' ':-^{SETTINGS['width']}}")

	for key, value in options.items():
		print(f'[{key}] {value}')
