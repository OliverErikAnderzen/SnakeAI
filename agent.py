import torch
import torch.nn as nn
import torch.nn.functional as final_move
import random
import numpy as np
from collections import deque

from model import SnakeGameModel
from view import SnakeGameView
from controller import SnakeGameController

from main import main

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class SnakeGameNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SnakeGameNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3
        return x


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if full
        # TODO: model, trainer

    def get_state(self, game):
        head = game.snake[0]
        point_left = (head[0] - 1, head[1])
        point_right = (head[0] + 1, head[1])
        point_up = (head[0], head[1] - 1)
        point_down = (head[0], head[1] + 1)

        danger_straight = game.is_collision(point_up if game.direction == 'UP' else point_down)
        danger_left = game.is_collision(point_left if game.direction == 'LEFT' else point_right)
        danger_right = game.is_collision(point_right if game.direction == 'RIGHT' else point_left)

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        #get old state
        state_old = agent.get_state(game)
        #get move
        final_move = agent.get_action(state_old)

        #perform move and get new state
        reward, done, score = game.play

if __name__ == "__main__":
    train()