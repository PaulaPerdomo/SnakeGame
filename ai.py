from typing import final
import torch 
import random
import numpy as np
from snake_game_ai import SnakeGame, Directions, Point
from collections import deque #stored memories

MAXIMUM_MEMORY = 100_000 
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class AI:

    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 #parameter to control randomness
        self.gamma = 0 #parameter to control discount rate
        self.memory = deque(maxlen=MAXIMUM_MEMORY) #if we exceed memory, it will begin to remove elements

    def get_state(self, game):

        #checks the 11 possible values
        head = game.snake[0]
        point_left = Point(head.x - 20, head.y)
        point_right = Point(head.x + 20, head.y)
        point_up = Point(head.x, head.y - 20)
        point_down = Point(head.x, head.y + 20)

        direction_left = game.direction == Directions.LEFT
        direction_right = game.direction == Directions.RIGHT
        direction_up = game.direction == Directions.UP
        direction_down = game.direction == Directions.DOWN

        #creates the list with 11 possible values. is_collision function takes in a point. 
        state = [

            #Danger straight. 
            (direction_left and game.is_collision(point_left)) or 
            (direction_right and game.is_collision(point_right)) or 
            (direction_up and game.is_collision(point_up)) or 
            (direction_down and game.is_collision(point_down)), 

            #Danger right. 
            (direction_left and game.is_collision(point_up)) or 
            (direction_right and game.is_collision(point_down)) or
            (direction_up and game.is_collision(point_right)) or 
            (direction_down and game.is_collision(point_left)), 

            #Direction left. 
            (direction_left and game.is_collision(point_down)) or 
            (direction_right and game.is_collision(point_up)) or
            (direction_up and game.is_collision(point_left)) or
            (direction_down and game.is_collision(point_right)), 

            #Move directions.
            direction_left, direction_right, direction_up, direction_down, 

            #Food location
            game.food.x < head.x, #food is left
            game.food.x > head.x, #food is right
            game.food.y < head.y, #food is up
            game.food.y > head.y #food is down
        ]

        #converts the state list into a numpy array will type int.
        return np.array(state, dtype= int)





    #for improvements!
    def remember(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = AI()
    game = SnakeGame()

    while True:
        #get the old state
        state_old = agent.get_state(game)

        #get move 
        final_move = agent.get_action(state_old)

        #perform move and get new state from game
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #remember --> store in memory
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #if game is over, train long memory which is also called replay/experience replay memory. 
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score

            print('Game', agent.number_of_games, 'Score', score, 'Record:', record)


#to call functions
if __name__ == '__main__':
    train()


