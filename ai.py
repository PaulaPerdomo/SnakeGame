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
        pass

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
            agent.train_long_memory

            if score > record:
                record = score

            print('Game', agent.number_of_games, 'Score', score, 'Record:', record)


#to call functions
if __name__ == '__main__':
    train()


