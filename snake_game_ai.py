#New things added for this version of snake_game
#reset 
#reward
#play(action) -> direction
#game_iteration
#is_collision

import pygame
from enum import Enum
from collections import namedtuple
import random
import numpy as np

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
SPEED = 10

Point = namedtuple('Point', 'x, y')

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        #display for pygame
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        #init game state
        self.direction = Directions.RIGHT
        self.score = 0
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCKSIZE, self.head.y), Point(self.head.x-(2*BLOCKSIZE), self.head.y)]
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        y = random.randint(0, (self.h-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food

    def play_step(self, action, ):

        self.frame_iteration += 1
        #collecting user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            
        #update the head of the snake in order to move
        self._move(self.action)
        self.snake.insert(0, self.head)

        #check if the game is over or there is no improvements. Also update reward for agent to learn
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        #place new food or move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()  

        #update the UI and clock
        self.update_ui()
        self.clock.tick(SPEED)
            
        #return game over and score
        return reward, game_over, self.score

    def _is_collision(self, pt=None):

        if pt is None:
            pt = self.head

        #hits the borders/boundary of the game
        if pt.x > self.w-BLOCKSIZE or pt.x < 0 or pt.y > self.h-BLOCKSIZE or pt.y < 0:
            return True
            
        #the snake hits itself 
        if pt in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        self.display.fill(BLACK)

        for i in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(i.x, i.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(i.x+4, i.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        #updates the screen 
        pygame.display.flip()
        
    #takes in the action from the agent 
    def _move(self, action):

        #possible movements: straight, right, left

        clock_wise = [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx] #remains the same
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx] #right turn 
        else:
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx] #left turn 

        self.direction = new_direction
        
        x = self.head.x
        y = self.head.y
            
        if self.direction == Directions.RIGHT:
            x += BLOCKSIZE
        elif self.direction == Directions.LEFT:
            x -= BLOCKSIZE
        elif self.direction == Directions.DOWN:
            y += BLOCKSIZE
        elif self.direction == Directions.UP:
            y -= BLOCKSIZE
            
        self.head = Point(x, y)



