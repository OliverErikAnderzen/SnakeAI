import random

class SnakeGameModel:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        self.FPS = 5
        self.segments = [(5, 5)]
        self.direction = "UP"
        self.food = self.generate_food_position()
        self.score = 0
        self.var_game_over = False

    def set_direction(self, newDirection):
        if newDirection == "DOWN":
            self.direction = newDirection
        elif newDirection == "UP":
            self.direction = newDirection
        elif newDirection == "RIGHT":
            self.direction = newDirection
        elif newDirection == "LEFT":
            self.direction = newDirection

    def turn_direction(self, newDirection):
        if newDirection == "DOWN" and self.direction != "UP":
            self.direction = newDirection
        elif newDirection == "UP" and self.direction != "DOWN":
            self.direction = newDirection
        elif newDirection == "RIGHT" and self.direction != "LEFT":
            self.direction = newDirection
        elif newDirection == "LEFT" and self.direction != "RIGHT":
            self.direction = newDirection

    def snake_collide(self):
        snake_head = self.segments[0]
        snake_body = self.segments[1:]
        return snake_head in snake_body

    def step_head(self, head):
        x, y = head
        if self.direction == "UP":
            return (x, y-1)
        if self.direction == "DOWN":
            return (x, y+1)
        if self.direction == "RIGHT":
            return (x+1, y)
        if self.direction == "LEFT":
            return (x-1, y)

    def step(self):
        new_position = None
        if self.eating():
            self.eat()
            return
        
        for i in range(len(self.segments)):
            if i == 0:
                new_position = self.segments[i]
                self.segments[i] = self.step_head(self.segments[i])
            else:
                old_position = self.segments[i]
                self.segments[i] = new_position
                new_position = old_position
                
    def generate_food_position(self):
        return (random.randint(0,19), random.randint(0,19))
    
    def new_food(self):
        #generate a random tuple
        new_position = self.generate_food_position()

        #set the new food position to random tuple
        self.food = new_position

    def eating(self):
        # is eating if the next step will be on the food position
        return self.step_head(self.segments[0]) == self.food

    def eat(self):
        # append foods position to front of segments DONE
        self.segments.insert(0,self.food)

        # create a new food position
        self.new_food()

    def out_of_bounds(self):
        x, y = self.segments[0]
        if x > 19 or x < 0:
            return True
        if y > 19 or y < 0:
            return True

    def game_over(self):
        if self.out_of_bounds() or self.snake_collide(): 
            self.var_game_over = True 

        return self.var_game_over
    
    def set_game_over(self, newState):
        if newState == True or newState == False:
            self.var_game_over = newState

    def get_state(self):
        return {
            "snake": self.snake,
            "food": self.food
        }