from settings import *

class Game:
    def __init__(self):
        self.display_info = pygame.display.Info()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.runnning = True
        self.fullscreen = False
        self.clock = pygame.time.Clock()

        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def toggle_windowed_fullscreen(self):
        self.fullscreen = not self.fullscreen
        window = gw.getWindowsWithTitle(WINDOW_CAPTION)[0]
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.display_info.current_w, self.display_info.current_h), pygame.NOFRAME)
            window.moveTo(0, 0)
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            window.moveTo(self.display_info.current_w // 2 - WINDOW_WIDTH // 2, self.display_info.current_h // 2 - WINDOW_HEIGHT // 2)
    
    def run(self):

        self.clock.tick(FPS)

        while self.runnning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runnning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_windowed_fullscreen()
                        

            self.WINDOW.fill((255, 255, 255))

            pygame.display.update()


game = Game()
if __name__ == "__main__":
    game.run()
        
pygame.quit()