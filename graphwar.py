# from curses import KEY_ENTER
from itertools import chain

import numpy as np
import pygame
from numpy import *
from pygame import KEYDOWN, QUIT, K_f, K_q
from player import Player
from position import Position

from utils import BLACK, CYAN, GRAY, GREEN, RED, WHITE



class GraphWar:
    LINE_WIDTH = 1
    PLOTING_STEP = 0.1
    SCALE_FACTOR = 10
    # FONT = pygame.font.SysFont('DejaVu Math TeX Gyre', 20)

    def __init__(self) -> None:
        pygame.init()
        self.board = pygame.display.set_mode((720, 720))
        self.board.fill(WHITE)
        self.O = Position(self.board.get_width() / 2, self.board.get_height() / 2)
        pygame.draw.line(
            self.board,
            BLACK,
            (self.O.x, 0),
            (self.O.x, self.board.get_height()),
            self.LINE_WIDTH,
        )  # Vertical Line
        pygame.draw.line(
            self.board,
            BLACK,
            (0, self.O.y),
            (self.board.get_width(), self.O.y),
            self.LINE_WIDTH,
        )  # Horizontal Line

        self.players = []

        self.add_player(geo_position=Player(-20, 5), team=CYAN)
        self.add_player(geo_position=Player(-13, 5), team=GRAY)
        self.add_player(geo_position=Player(25, 15), team=GRAY)
        self.add_player(geo_position=Player(14, -6), team=GRAY)
        self.add_player(geo_position=Player(-7, -15), team=GRAY)

    def geometric_to_pygame(self, geo_position):
        return Position(geo_position.x * self.SCALE_FACTOR + self.O.x, self.O.y - geo_position.y * self.SCALE_FACTOR)

    def pygame_to_geometric(self, pygame_position):
        pass

    def add_player(self, geo_position, team) -> None:
        self.players.append(geo_position)
        pygame.draw.circle(
            self.board,
            team,
            self.geometric_to_pygame(geo_position),
            Player.PLAYER_RADIUS,
            Player.PLAYER_WIDTH,
        )

    def plot(self, player, func):

        iter_r = arange(player.x, self.O.x / self.SCALE_FACTOR, self.PLOTING_STEP)
        iter_l = arange(player.x-self.PLOTING_STEP, -self.O.x / self.SCALE_FACTOR, -self.PLOTING_STEP)

        X = array(list(chain(*zip(iter_l, iter_r))))
        Y = func(X)

        C = func(player.x)
        print(f'{C=} = func({player.x=})\t\t{player.y=}')
        rmissle_hit = None
        lmissle_hit = None

        for x, y in zip(X, Y):
            x_translated = x
            y_translated = y + (player.y - C)

            if lmissle_hit is not None and x_translated < lmissle_hit.x:
                continue
            if rmissle_hit is not None and x_translated > rmissle_hit.x:
                continue


            pygame.draw.circle(
                self.board, BLACK, self.geometric_to_pygame(geo_position=Position(x_translated, y_translated)), 1, 1
            )
            for _player in filter(lambda p: p is not player, self.players):
                if _player.is_hit(x_translated, y_translated):
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(geo_position=_player),
                        self.geometric_to_pygame(geo_position=_player + Position(1, 1)),
                        self.LINE_WIDTH*4,
                    )
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(geo_position=_player),
                        self.geometric_to_pygame(geo_position=_player + Position(-1, -1)),
                        self.LINE_WIDTH*4,
                    )
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(geo_position=_player),
                        self.geometric_to_pygame(geo_position=_player + Position(1, -1)),
                        self.LINE_WIDTH*4,
                    )
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(geo_position=_player),
                        self.geometric_to_pygame(geo_position=_player + Position(-1, 1)),
                        self.LINE_WIDTH*4,
                    )
                    if _player.x >= player.x:
                        rmissle_hit = Position(_player.x, _player.y)
                    else:
                        lmissle_hit = Position(_player.x, _player.y)

            pygame.display.flip()
        self.ploting = False


    def start(self):

        self.ploting = True
        self.playing = True
        while self.playing:

            for e in pygame.event.get():

                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_q):
                    exit()
                elif (e.type == KEYDOWN and e.key == K_f) and self.ploting:
                    # self.plot(self.players[0], lambda x: sin((x / 4) - 0.5))
                    # self.plot(self.players[0], lambda x: 0*x + 5)
                    self.plot(self.players[0], lambda x: 6*sin(x/5))

            pygame.display.flip()


if __name__ == "__main__":
    GraphWar().start()
