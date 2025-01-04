import pygame
import random

grid_size = (20, 20)
cell_size = 20


snake_direction = "North"
snake_position = [5, 5]

def resetSnakePosition():
    global snake_position
    snake_position = [5, 5]

BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

pygame.init()
screen = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
pygame.display.set_caption("SnakeAI")

clock = pygame.time.Clock()
FPS = 3

def getNewCherryPosition():
    return (random.randint(0, 19), random.randint(0, 19))

def drawNewCherry():
    position = getNewCherryPosition()
    pygame.draw.rect(screen, RED, (cell_size*position[0], cell_size*position[1], 20, 20))
    

def drawSnake():
    pygame.draw.rect(screen, GREEN, (cell_size*snake_position[0],cell_size*snake_position[1],20,20))

def checkGameOver():
    if snake_position[0] > 19 or snake_position[0] < 0 or snake_position[1] > 19 or snake_position[1] < 0:
        print("GAME OVER")
        return True
    return False

def moveSnakePosition():
    if snake_direction == "North":
        snake_position[1] = snake_position[1] - 1
    elif snake_direction == "South":
        snake_position[1] = snake_position[1] + 1
    elif snake_direction == "East":
        snake_position[0] = snake_position[0] + 1
    elif snake_direction == "West":
        snake_position[0] = snake_position[0] - 1

def setSnakeDirection(key, waiting):
    global snake_direction
    if key == 79 and (snake_direction == "North" or snake_direction == "South" or waiting):
        snake_direction = "East"
    elif key == 80 and (snake_direction == "North" or snake_direction == "South" or waiting):
        snake_direction = "West"
    elif key == 81 and (snake_direction == "East" or snake_direction == "West" or waiting):
        snake_direction = "South"
    elif key == 82 and (snake_direction == "East" or snake_direction == "West" or waiting):
        snake_direction = "North"

def runGame():
    ### Waiting loop
    waiting = True
    running = False

    font = pygame.font.Font(None, 36)

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.scancode:
                code = event.scancode
                if code >= 79 and code <= 82:
                    setSnakeDirection(code, True)
                    running = True
                    waiting = False
        screen.fill((0,0,0))

        text = font.render("Press the arrow keys to start", True, (255,255,255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)

        drawSnake()
        pygame.display.flip() #redraws the screen
        clock.tick(FPS)

    ### Running Loop
    while running:
        if checkGameOver():
            running = False

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False
            # if code == 41:
            #     running = False
            #     resetSnakePosition()
            #     runGame()
            if event.type == pygame.KEYDOWN:
                setSnakeDirection(event.scancode, False)
            
        moveSnakePosition()

        screen.fill((0,0,0))

        drawSnake()
        drawNewCherry()

        pygame.display.flip() #redraws the screen

        clock.tick(FPS)



if __name__ == "__main__":
    runGame()