# SnakeAI
Snake AI Bot

We have implemented a simple version of Snake, using MVC pattern.

Now we need to make an AI agent which can play the game and learn from it.

1. State (position of game elements)
2. Action (which possible actions it can take)
3. Reward (feedback on how it is doing) 
    * + for eating food
    * - for colliding with wall or itself
    * - for taking a step which doesnt eat to reduce inefficency
