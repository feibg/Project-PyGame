from settings import *
from sprites import *
from groups import *
import pygetwindow as gw

class Game:
    def __init__(self):
        self.display_info = pygame.display.Info()
        self.WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.runnning = True
        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.game_started = False

        self.all_sprites = AllSprites()

        self.player_surf = pygame.Surface((50, 50))
        self.player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), self.player_surf, self.all_sprites)

        self.setup()

    def setup(self):
        tmx_map = load_pygame(join('data', 'tmx', 'Test.tmx'))
        self.level_width = tmx_map.width * tmx_map.tilewidth
        self.level_height = tmx_map.height * tmx_map.tileheight

        for x, y, image in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), image, self.all_sprites)
        
    def toggle_windowed_fullscreen(self):
        self.fullscreen = not self.fullscreen
        window = gw.getWindowsWithTitle(WINDOW_CAPTION)[0]
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.display_info.current_w, self.display_info.current_h), pygame.NOFRAME)
            window.moveTo(0, 0)
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            window.moveTo(self.display_info.current_w // 2 - WINDOW_WIDTH // 2, self.display_info.current_h // 2 - WINDOW_HEIGHT // 2)
    
    def menu(self):
        while not self.game_started:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runnning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_started = True

            self.WINDOW.fill((50, 50, 50))
            pygame.display.update()

    def run(self):

        while self.runnning:

            dt = self.clock.tick(FPS) / 1000
            
            if not self.game_started:
                self.menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runnning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_windowed_fullscreen()   

            self.all_sprites.update(dt)

            self.WINDOW.fill((50, 50, 50))
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
        
pygame.quit()