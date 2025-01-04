import pygame

grid_size = (20, 20)
cell_size = 20


snake_direction = "North"
snake_position = [5, 5]

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

pygame.init()
screen = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
pygame.display.set_caption("SnakeAI")

clock = pygame.time.Clock()
FPS = 2

def drawSnake():
    pygame.draw.rect(screen, GREEN, (cell_size*snake_position[0],cell_size*snake_position[1],20,20))
    print(snake_position)

def moveSnakePosition():
    if snake_direction == "North":
        snake_position[1] = snake_position[1] - 1
    elif snake_direction == "South":
        snake_position[1] = snake_position[1] + 1
    elif snake_direction == "East":
        snake_position[0] = snake_position[0] + 1
    elif snake_direction == "West":
        snake_position[0] = snake_position[0] - 1

def setSnakeDirection(key):
    global snake_direction
    if key == 79:
        snake_direction = "East"
    elif key == 80:
        snake_direction = "West"
    elif key == 81:
        snake_direction = "South"
    elif key == 82:
        snake_direction = "North"

def runGame():
    running = False
    
    while running:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                setSnakeDirection(event.scancode)
            
        screen.fill((0,0,0))

        drawSnake()

        moveSnakePosition()

        pygame.display.flip() #redraws the screen

        clock.tick(FPS)



if __name__ == "__main__":
    runGame()