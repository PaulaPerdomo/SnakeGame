import pygame
from enum import Enum
from collections import namedtuple
import random

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

#reset 
#reward
#play(action) -> direction
#game_iteration
#is_collision

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

        #game state
        self.direction = Directions.RIGHT
        self.score = 0
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCKSIZE, self.head.y), Point(self.head.x-(2*BLOCKSIZE), self.head.y)]
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        y = random.randint(0, (self.h-BLOCKSIZE)//BLOCKSIZE)*BLOCKSIZE
        self.food = Point(x, y)
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
            
        #update the head of the snake in order to move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        #check if the game is over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        #place new food or move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()  

        #update the UI and clock
        self.update_ui()
        self.clock.tick(SPEED)
            
        #return game over and score
        return game_over, self.score

    def _is_collision(self):

        #hits the borders/boundary of the game
        if self.head.x > self.w-BLOCKSIZE or self.head.x < 0 or self.head.y > self.h-BLOCKSIZE or self.head.y < 0:
            return True
            
        #the snake hits itself 
        if self.head in self.snake[1:]:
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
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
            
        if direction == Directions.RIGHT:
            x += BLOCKSIZE
        elif direction == Directions.LEFT:
            x -= BLOCKSIZE
        elif direction == Directions.DOWN:
            y += BLOCKSIZE
        elif direction == Directions.UP:
            y -= BLOCKSIZE
            
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()

    #game loop 
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()


