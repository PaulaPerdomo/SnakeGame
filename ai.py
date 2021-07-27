from typing import final
import torch 
import random
import numpy as np
from snake_game_ai import SnakeGame, Directions, Point
from collections import deque #stored memories
from model import Linear_QNet, QTrainer

MAXIMUM_MEMORY = 100_000 
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class AI:

    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 #parameter to control randomness
        self.gamma = 0.9 #parameter to control discount rate. Needs to be smaller than 1
        self.memory = deque(maxlen=MAXIMUM_MEMORY) #if we exceed memory, it will begin to remove elements
        self.model = Linear_QNet(11, 256, 3) #11 inputs and 3 outputs. 256 can be changed
        self.trainer = QTrainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)

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
        self.memory.append((state, action, reward, next_state, done)) #remember that memory is a deque. Store as a tuple

    def get_action(self, state):
        #random moves: tradeoff exploration/explotation
        self.epsilon = 80 - self.number_of_games #hardcoded. The more games we have the smaller epsilon will get
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item() #makes an integer
            final_move[move] = 1

        return final_move

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory > BATCH_SIZE):
            mini_sample = random.sample(self.memory, BATCH_SIZE) #returns a list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample) #can also be done with a for loop

        #since it with be training lots of data
        self.trainer.train_step(states, actions, rewards, next_states, dones)



    

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
                agent.model.save()

            print('Game', agent.number_of_games, 'Score', score, 'Record:', record)


#to call functions
if __name__ == '__main__':
    train()


