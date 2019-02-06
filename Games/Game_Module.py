from os import environ
from pygame import init, display, time


class Game():

    def __init__(self, game_title, width, height, key_to_events):
        environ['SDL_VIDEO_CENTERED'] = '1'

        init()
        self.screen = display.set_mode((width, height))

        display.set_caption(game_title)
        self.clock = time.Clock()

        Game.KEY_TO_EVENTS = key_to_events
