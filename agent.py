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
        x = self.fc3(x)
        return x


class Agent:
    def __init__(self, reset_model=True):
        self.n_games = 0
        self.epsilon = 300 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() if full
        
        if reset_model:
            print("🧠 Initializing a NEW neural network!")
            self.model = SnakeGameNN(input_size=11, hidden_size=512, output_size=3)  # New model
        else:
            print("🔁 Using the previous trained model!")

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = nn.SmoothL1Loss()

    def get_state(self, game):
        head = game.snake[0]
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


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self._train_step(states, actions, rewards, next_states, dones)   

    def train_short_memory(self, state, action, reward, next_state, done):
        self._train_step(state, action, reward, next_state, done)
        

    def get_action(self, state):
        self.epsilon = max(1, 150 - self.n_games)  # Allows longer exploration

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            # print(f"🔄 Random Move Chosen: {move}")  # Debug
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            move = torch.argmax(prediction).item()
            # print(f"🧠 Model Move Chosen: {move}")  # Debug
        return move


        final_move[move] = 1
        return final_move

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