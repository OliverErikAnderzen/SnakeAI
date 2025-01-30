import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import numpy as np
import time
from collections import deque

from model import SnakeGameModel
from view import SnakeGameView
from controller import SnakeGameController

# from main import main

MAX_MEMORY = 100_000
BATCH_SIZE = 2000
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

    # def __init__(self, input_size, hidden_size, output_size):
    #     super(SnakeGameNN, self).__init__()
    #     self.fc1 = nn.Linear(input_size, hidden_size)
    #     self.fc2 = nn.Linear(hidden_size, hidden_size)
    #     self.fc3 = nn.Linear(hidden_size, hidden_size // 2)  # Extra layer for depth
    #     self.fc4 = nn.Linear(hidden_size // 2, output_size)

    # def forward(self, x):
    #     x = F.relu(self.fc1(x))
    #     x = F.relu(self.fc2(x))
    #     x = F.relu(self.fc3(x))  # New hidden layer
    #     x = self.fc4(x)
    #     return x

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
        head = game.segments[0]
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

    def _train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        prediction = self.model(state)
        target = prediction.clone()

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx])).item()
            else:
                Q_new = reward[idx]  # No future reward if the game is over

            target[idx][torch.argmax(action[idx]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction)
        loss.backward()
        self.optimizer.step()

        print(f"📉 Training Loss: {loss.item()}")  # Debugging to track learning


def train():
    agent = Agent()
    game = SnakeGameModel((20, 20))
    view = SnakeGameView(game)  
    high_score = 0

    while True:
        state_old = agent.get_state(game)

        food_x, food_y = game.food
        head_x, head_y = game.segments[0]  # Get snake head position
        prev_distance = abs(food_x - head_x) + abs(food_y - head_y)

        move = agent.get_action(state_old)

        # 🔄 Convert move (0,1,2) to "UP", "DOWN", etc.
        direction_map = {
            0: game.direction,  # 0 means go straight, so keep current direction
            1: {"UP": "LEFT", "DOWN": "RIGHT", "LEFT": "DOWN", "RIGHT": "UP"}[game.direction],  # Left
            2: {"UP": "RIGHT", "DOWN": "LEFT", "LEFT": "UP", "RIGHT": "DOWN"}[game.direction],  # Right
        }
        new_direction = direction_map[move]

        # print(f"Before move: {game.direction}, Move: {move} → After move: {new_direction}")  # Debugging

        game.turn_direction(new_direction)  # Pass the correct string direction
        game.step()

        new_head_x, new_head_y = game.segments[0]
        new_distance = abs(food_x - new_head_x) + abs(food_y - new_head_y)

        view.render()
        time.sleep(0.01)  # Slow down the game

        if game.game_over():
            reward = -1000  # 🚨 Strong penalty for dying
        elif game.eating():
            reward = 500  # 🍎 Large reward for eating food
        else:
            if new_distance < prev_distance:
                reward = 10  # 👍 Bigger reward for getting closer
            elif new_distance > prev_distance:
                reward = -10  # ❌ Higher penalty for moving away
            else:
                reward = -5  # 👎 Small penalty for staying in place
            
            reward += 0.2  # 🏆 Small bonus for staying alive


        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, move, reward, state_new, game.game_over())
        agent.remember(state_old, move, reward, state_new, game.game_over())

        if game.game_over():
            score = game.score  
            if score > high_score:
                high_score = score

            # print(f"Game: {agent.n_games}, Score: {score}, High Score: {high_score}")

            game.reset()
            agent.n_games += 1


if __name__ == "__main__":
    train()