class SnakeGameModel:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        self.snake = [(5, 5)]
        self.food = (10, 10)
        self.score = 0
        self.game_over = False

    def step(self, action):
        pass

    def is_game_over(self):
        return self.game_over

    def get_state(self):
        return {
            "snake": self.snake,
            "food": self.food
        }