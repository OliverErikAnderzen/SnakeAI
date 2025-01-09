import pygame

class SnakeGameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_player_input(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                self.model.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return "UP"
                elif event.key == pygame.K_DOWN:
                    return "DOWN"
                elif event.key == pygame.K_LEFT:
                    return "LEFT"
                elif event.key == pygame.K_RIGHT:
                    return "RIGHT"
        return None

    def run(self):
        clock = pygame.time.Clock()
        while not self.model.is_game_over():
            action = self.get_player_input()
            if action == "QUIT":
                break
            if action:
                self.model.set_direction(action)
            self.model.step()
            self.view.render()
            clock.tick(self.model.FPS)

        print(f"Game Over! Your score: {self.model.score}")
