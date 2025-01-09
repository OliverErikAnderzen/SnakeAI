class SnakeGameModel:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        self.FPS = 5
        self.segments = [(5, 5)]
        self.direction = "UP"
        self.food = (15, 15)
        self.score = 0
        self.game_over = False

    def set_direction(self, newDirection):
        if newDirection == "DOWN" and self.direction != "UP":
            self.direction = newDirection
        elif newDirection == "UP" and self.direction != "DOWN":
            self.direction = newDirection
        elif newDirection == "RIGHT" and self.direction != "LEFT":
            self.direction = newDirection
        elif newDirection == "LEFT" and self.direction != "RIGHT":
            self.direction = newDirection

    def step_segment(self, segment):
        x, y = segment
        if self.direction == "UP":
            return (x, y-1)
        if self.direction == "DOWN":
            return (x, y+1)
        if self.direction == "RIGHT":
            return (x+1, y)
        if self.direction == "LEFT":
            return (x-1, y)

    def step(self):
        self.segments = [self.step_segment(segment) for segment in self.segments]
        print(self.segments)

    def is_out_of_bounds(self):
        x, y = self.segments[0]
        if x > 19 or x < 0:
            return True
        if y > 19 or y < 0:
            return True

    def is_game_over(self):
        if self.is_out_of_bounds(): self.game_over = True 

        return self.game_over

    def get_state(self):
        return {
            "snake": self.snake,
            "food": self.food
        }