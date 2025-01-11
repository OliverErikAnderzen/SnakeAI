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
    
    def wait_for_button_press(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"  # Return "QUIT" to exit the game
                elif event.type == pygame.KEYDOWN:  # Key press detected
                    return event.key  # Return the key pressed
            # You can also add a small delay to reduce CPU usage
            self.view.render()
            pygame.time.wait(10)

    def run(self):
        clock = pygame.time.Clock()

        if self.wait_for_button_press() == "QUIT":
            return

        while not self.model.is_game_over():
            action = self.get_player_input()
            if action == "QUIT":
                break
            if action:
                self.model.set_direction(action)
            self.model.step()
            self.model.check_snake_collide()
            self.view.render()
            clock.tick(self.model.FPS)

        print(f"Game Over! Your score: {len(self.model.segments)-1}")
