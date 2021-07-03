import pygame
from enum import Enum
from collections import namedtuple
import random

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Directions(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

BLACK =  (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)

BLOCKSIZE= 20
SPEED = 20

point = namedtuple('Point', 'x, y')

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        #display for pygame
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.clock()

        #game state
        self.direction = Directions.RIGHT
        self.score = 0
        self.head = point(self.w/2, self.h/2)
        self.snake = [self.head, point(self.head.x-BLOCKSIZE, self.head.y), point(self.head.x-(2*BLOCKSIZE), self.head.y)]
        self.food = None
        self._place_food()

        def _place_food(self):
            x = random.randint(0, (self.w-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
            y = random.randint(0, (self.h-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
            self.food = point(x, y)
            if self.food in self.snake:
                self._place_food

        def play_step(self):

            #collecting user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = Directions.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.direction = Directions.RIGHT
                    elif event.key == pygame.K_UP:
                        self.direction = Directions.UP
                    elif event.key == pygame.K_DOWN:
                        self.direction = Directions.DOWN
            

            #update the head of the snake
print(3)