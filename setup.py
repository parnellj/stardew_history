try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'Stardew History',
	'version': '0.1',
	'url': 'https://github.com/parnellj/stardew_history',
	'download_url': 'https://github.com/parnellj/stardew_history',
	'author': 'Justin Parnell',
	'author_email': 'parnell.justin@gmail.com',
	'maintainer': 'Justin Parnell',
	'maintainer_email': 'parnell.justin@gmail.com',
	'classifiers': [],
	'license': 'GNU GPL v3.0',
	'description': 'Preserves daily saved games and visualizes farm buildup over time for the game Stardew Valley.',
	'long_description': 'Preserves daily saved games and visualizes farm buildup over time for the game Stardew Valley.',
	'keywords': '',
	'install_requires': ['nose'],
	'packages': ['stardew_history'],
	'scripts': []
}
	
setup(**config)
