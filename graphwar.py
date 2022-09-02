# from curses import KEY_ENTER
from collections import namedtuple
from itertools import chain

import numpy as np
import pygame
from numpy import *
from pygame import KEYDOWN, QUIT, K_f, K_q

from utils import BLACK, GREEN, RED, WHITE, GRAY, CYAN

# Position = namedtuple('Positon', 'x y')


class Position(tuple):
    def __new__(cls, x, y):
        self = super().__new__(cls, (x, y))
        return self

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
    
    @property
    def radius(self):
        return 2

    def __add__(self, position):
        new_x = self.x + position.x
        new_y = self.y + position.y
        return self.__new__(self.__class__, new_x, new_y)
    
    def is_hit(self, x, y):
        return (
            self.x - self.radius <= x <= self.x + self.radius
            and self.y - self.radius <= y <= self.y + self.radius
        )
        


Player = Position


class GraphWar:
    LINE_WIDTH = 1
    PLAYER_WIDTH = 4
    PLAYER_RADIUS = 5
    PLOTING_STEP = 0.3
    # FONT = pygame.font.SysFont('DejaVu Math TeX Gyre', 20)

    def __init__(self) -> None:
        pygame.init()
        self.board = pygame.display.set_mode((920, 720))
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

        self.add_player(Position(0, 10), CYAN)
        self.add_player(Position(27, 10), GRAY)

    def geometric_to_pygame(self, position):
        return Position(position.x * 10 + self.O.x, self.O.y - position.y * 10)

    def add_player(self, position, team) -> None:
        self.players.append(position)
        pygame.draw.circle(
            self.board,
            team,
            self.geometric_to_pygame(position),
            self.PLAYER_RADIUS,
            self.PLAYER_WIDTH,
        )

    def hit_player(self) -> None:
        pass

    def plot(self, player, func):
        iter_r = arange(0, self.O.x, self.PLOTING_STEP)
        iter_l = arange(-self.PLOTING_STEP, -self.O.x, -self.PLOTING_STEP)

        X = np.array(list(chain(*zip(iter_l, iter_r))))
        X = np.array(list(iter_r))
        Y = func(X)

        for x, y in zip(X, Y):
            x = player.x + x
            y = player.y + y

            pygame.draw.circle(self.board, BLACK, self.geometric_to_pygame(Position(x, y)), 1, 1)
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

                    # pygame.draw.circle(self.board, RED, self.geometric_to_pygame(self.O), self.PLAYER_RADIUS, self.PLAYER_WIDTH)
                    
                    self.ploting = False
                    break

            pygame.display.flip()

        else:
            self.ploting = False

    def start(self):

        self.ploting = True
        self.playing = True
        while self.playing:

            for e in pygame.event.get():

                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_q):
                    exit()
                else:
                    if (e.type == KEYDOWN and e.key == K_f) and self.ploting:
                        # self.plot(self.players[0], lambda x: sin((x / 4) - 0.5))
                        self.plot(self.players[0], lambda x: x/x - 1)

            pygame.display.flip()


if __name__ == "__main__":
    GraphWar().start()
