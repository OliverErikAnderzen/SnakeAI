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
        x = self.fc3(x)
        return x


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if full
        # TODO: model, trainer
        self.model = SnakeGameNN(input_size=11, hidden_size=256, output_size=3)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.MSELoss()

    def get_state(self, game):
        head = game.snake[0]
        point_left = (head[0] - 1, head[1])
        point_right = (head[0] + 1, head[1])
        point_up = (head[0], head[1] - 1)
        point_down = (head[0], head[1] + 1)
        direction = game.direction
        food = game.food

        point_straight = (
            (head[0], head[1] - 1) if direction == "UP" else
            (head[0], head[1] + 1) if direction == "DOWN" else
            (head[0] - 1, head[1]) if direction == "LEFT" else
            (head[0] + 1, head[1])  # RIGHT
        )
        point_left = (
            (head[0] - 1, head[1]) if direction == "UP" else
            (head[0] + 1, head[1]) if direction == "DOWN" else
            (head[0], head[1] + 1) if direction == "LEFT" else
            (head[0], head[1] - 1)  # RIGHT
        )
        point_right = (
            (head[0] + 1, head[1]) if direction == "UP" else
            (head[0] - 1, head[1]) if direction == "DOWN" else
            (head[0], head[1] - 1) if direction == "LEFT" else
            (head[0], head[1] + 1)  # RIGHT
        )


        # Check if these points are dangerous
        danger_straight = (
            point_straight in game.segments or
            point_straight[0] < 0 or
            point_straight[1] < 0 or
            point_straight[0] >= game.grid_size[0] or
            point_straight[1] >= game.grid_size[1]
        )
        danger_left = (
            point_left in game.segments or
            point_left[0] < 0 or
            point_left[1] < 0 or
            point_left[0] >= game.grid_size[0] or
            point_left[1] >= game.grid_size[1]
        )
        danger_right = (
            point_right in game.segments or
            point_right[0] < 0 or
            point_right[1] < 0 or
            point_right[0] >= game.grid_size[0] or
            point_right[1] >= game.grid_size[1]
        )

        # Normalize direction and food locations
        state = [
            # Danger zones
            danger_straight,
            danger_left,
            danger_right,

            # Move direction
            direction == "LEFT",
            direction == "RIGHT",
            direction == "UP",
            direction == "DOWN",

            # Food location
            food[0] < head[0],  # Food left
            food[0] > head[0],  # Food right
            food[1] < head[1],  # Food up
            food[1] > head[1],  # Food down
        ]
        return np.array(state, dtype=int)

        danger_straight = game.is_collision(point_up if game.direction == 'UP' else point_down)
        danger_left = game.is_collision(point_left if game.direction == 'LEFT' else point_right)
        danger_right = game.is_collision(point_right if game.direction == 'RIGHT' else point_left)

    def remember(self, state, action, reward, next_state, done):
        pass
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        pass
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

    def train_short_memory(self):
        pass
        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self._train_step(states, actions, rewards, next_states, dones)   

    def train_short_memory(self, state, action, reward, next_state, done):
        self._train_step(state, action, reward, next_state, done)
        

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