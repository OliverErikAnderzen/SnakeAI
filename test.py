import pygame

grid_size = (20, 20)
cell_size = 20

snake_position = (5, 5)

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

pygame.init()
screen = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
pygame.display.set_caption("SnakeAI")


def runGame():
    running = True
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
            
            screen.fill((0,0,0))

            



if __name__ == "__main__":
    runGame()