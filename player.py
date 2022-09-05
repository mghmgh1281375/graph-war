


# class Player:

#     radius = 4

#     def __init__(self, x, y) -> None:
#         # Relative to O
#         self.x = x
#         self.y = y
    
#     def translate2screen(self, Ox, Oy):
#         return self.x + Ox, (Oy - self.y)
    
#     def translate2player(self, x, y):
#         return x + self.x, (self.y - y)
    
#     def is_hit(self, x, y):
#         return (x - self.x)**2 + (y - self.y)**2 <= self.radius**2


from position import Position


class Player(Position):
    PLAYER_WIDTH = 4
    PLAYER_RADIUS = 5

    def is_hit(self, x, y):
        return ((x-self.x)**2 + (y-self.y)**2) <= self.PLAYER_RADIUS**2
