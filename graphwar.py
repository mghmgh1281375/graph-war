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

    def add_player(self, position, team) -> None:
        self.players.append(position)
        pygame.draw.circle(
            self.board,
            team,
            self.geometric_to_pygame(position),
            PLAYER_RADIUS,
            PLAYER_WIDTH,
        )

    def plot(self, player, func):
        iter_r = arange(0, self.O.x, self.PLOTING_STEP)
        iter_l = arange(-self.PLOTING_STEP, -self.O.x, -self.PLOTING_STEP)

        X = np.array(list(chain(*zip(iter_l, iter_r))))
        X = np.array(list(iter_r))
        Y = func(X)

        for x, y in zip(X, Y):
            x = player.x + x
            y = player.y + y

            pygame.draw.circle(
                self.board, BLACK, self.geometric_to_pygame(Position(x, y)), 1, 1
            )
            pygame.display.flip()
        self.ploting = False

        for x, y in zip(X, Y):
            x = player.x + x
            y = player.y + y
            for player in self.players:
                if player.is_hit(x, y):
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(player),
                        self.geometric_to_pygame(player + Position(1, 1)),
                        self.LINE_WIDTH,
                    )
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(player),
                        self.geometric_to_pygame(player + Position(-1, -1)),
                        self.LINE_WIDTH,
                    )
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(player),
                        self.geometric_to_pygame(player + Position(1, -1)),
                        self.LINE_WIDTH,
                    )
                    pygame.draw.line(
                        self.board,
                        RED,
                        self.geometric_to_pygame(player),
                        self.geometric_to_pygame(player + Position(-1, 1)),
                        self.LINE_WIDTH,
                    )

    def start(self):

        self.ploting = True
        self.playing = True
        while self.playing:

            for e in pygame.event.get():

                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_q):
                    exit()
                elif (e.type == KEYDOWN and e.key == K_f) and self.ploting:
                    # self.plot(self.players[0], lambda x: sin((x / 4) - 0.5))
                    self.plot(self.players[0], lambda x: x / x - 1)

            pygame.display.flip()


if __name__ == "__main__":
    GraphWar().start()
