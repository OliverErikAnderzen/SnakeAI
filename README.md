# SnakeAI
Snake AI Bot

How to implement a AI agent which can play snake

Im not going to go into detail about the game logic but i will talk only about the AI agent as that is my focus to learn.

## The AI Agent

### Neural Network
Make a very simple neural network
- **Input layer**: 11 neurons
- **Hidden layer**: 256 neurons
- **Output layer**: 3 neurons

The Input layer has 11 neurons because it takes a game-state np.array with 11 boolean values. The output layer has 3 neurons because it has to choose between three actions, LEFT, UP or RIGHT.

We are using the ReLU activation function as we pass the values between the layers. This makes all negative values to 0.

![alt text](<readme_images/Screenshot 2025-01-30 132501.png>)

### Q-learning
The neural network is using Q-learning. The Q-value stands for the future reward after taking a certain action in a specific state; Q(s, a). Higher Q-value is better. Using the NN, the agent learns to predict Q-values.

The agent interacts with the enviroment by
* observing state
* taking action
* recieving reward
* changing state (by taking action)

![Deep Q-learning formula](<readme_images/Screenshot 2025-01-30 131309.png>)

### The Agent Class
The Agent controls the decisions made and the training of the model.

important variables
- **epsilon**: Chooses if the model should be exploring or exploiting.
- **gamma**: Sets the importance of future rewards.
- **memory**: A deque, used to store experiences.
- **optimizer**: updates the weights to reduce the loss, Adam is great.
- **criterion**: (loss function), calculates how wrong the model is at predicting.

### Memory
Experiences can be saved and discarded from the deque self.memory.

#### train short memory
This is done after every step, where the model is trained on just the last action.

#### train long memory
This is done on a batch of past experiences. It then learns from random past experiences, if batch-size = 3000, it takes 3000 past experiences at random and trains upon. Its run after each game ends.