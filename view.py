import pygame

class SnakeGameView:
    def __init__(self, model):
        pygame.init()
        self.model = model
        self.grid_size = model.grid_size
        self.cell_size = 20
        self.screen = pygame.display.set_mode(
            (self.grid_size[0] * self.cell_size, self.grid_size[1] * self.cell_size) 
        )
        pygame.display.set_caption("SnakeAI")

    def draw_segment(self, x, y, color):
        pygame.draw.rect(self.screen, color,
                             (x * self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
            
    def draw_food(self):
        red = (255,0,0)
        fx, fy = self.model.food
        self.draw_segment(fx, fy, red)
        

    def render(self):
        self.screen.fill((0, 0, 0))

        for segment in self.model.segments:
            x, y = segment
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (x * self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
            
        fx, fy = self.model.food
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (fx * self.cell_size, fy * self.cell_size, self.cell_size, self.cell_size))

        pygame.display.flip()
