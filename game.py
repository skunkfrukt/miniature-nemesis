GAME_VERSION = "0.0.2"

import argparse
from src import world

import logging
logging.basicConfig()
log = logging.getLogger()


parser = argparse.ArgumentParser(description="A danmaku runner.")
parser.add_argument('-v', '--version', action='version', version=GAME_VERSION)
parser.add_argument('-fs', '--fullscreen', action='store_true',
    dest='fullscreen', help='launch the game in fullscreen mode')
logging_options = parser.add_mutually_exclusive_group()
logging_options.add_argument('--debug', action='store_const', dest='logging_level', const=logging.DEBUG, help='log DEBUG-level messages')
logging_options.add_argument('--info', action='store_const', dest='logging_level', const=logging.INFO, help='log INFO-level messages')
logging_options.add_argument('--warning', action='store_const', dest='logging_level', const=logging.WARNING, help='log WARNING-level messages')
parser.set_defaults(logging_level=logging.ERROR)
args = parser.parse_args()

log_level = logging.DEBUG  ## log_level = args.logging_level
log.setLevel(log_level)
log.info('{} logging enabled.'.format(logging.getLevelName(log_level)))

import pyglet

pyglet.font.add_directory('fonts')

log.info('Loading game data.')

from src import worldbuilder

worldbuilder.json_to_world('data/world.json')

from src import gui

log.info('Launching game.')

gui.MainWindow(fullscreen=args.fullscreen)

pyglet.app.run()

log.info('Exiting game.')
