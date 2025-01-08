from model import SnakeGameModel
from view import SnakeGameView
from controller import SnakeGameController
import pygame

def main():
    pygame.init()
    # Initialize the model
    grid_size = (20, 20)  # Example grid size
    model = SnakeGameModel(grid_size)

    # Initialize the view
    view = SnakeGameView(model)

    # Initialize the controller
    controller = SnakeGameController(model, view)

    # Run the game
    controller.run()

if __name__ == "__main__":
    main()
