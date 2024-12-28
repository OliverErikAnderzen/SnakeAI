import pygame



grid_size = (20, 20)
cell_size = 20

pygame.init()
screen = pygame.display.set_mode((grid_size[0]*cell_size, grid_size[1]*cell_size))
screen.fill((0,0,0))

running = True
while running:
    for event in pygame.event.get():