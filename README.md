# SnakeAI
Snake AI Bot

Implement a simple version of Snake, using MVC pattern.

How to make an AI agent which can play the game and learn from it.

1. State (position of game elements)
    Give the game agent info about what moves it shouldnt take, where the food is, where itself (the snake head) is, and what direction it has. 
    Convert the state info into an array, and normalize the booleans into integers
    ## return np.array(state, dtype=int)

2. Action (which possible actions it can take)

3. Reward (feedback on how it is doing) 
    * + 10 for eating food
    * - 20 for colliding with wall or itself
    * - 1  for taking a step which doesnt eat to reduce inefficency
    '

# More
1. Memory 
    The remember function is used to save previous experiences, it takes the 
    (state, action, reward, next_state, done) and keeps it in memory (deque).
    We train the model on the memory.
