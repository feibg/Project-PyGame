from settings import *
from support import *
from sprites import *
from groups import *
import pygetwindow as gw

class Game:
    def __init__(self):
        self.display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.running = True
        self.fullscreen = False
        self.zoom = 2.5
        self.clock = pygame.time.Clock()
        self.game_started = False
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.all_sprites = AllSprites(self.game_surface)

        self.load_assets()
        self.setup()

    def load_assets(self):
        self.player_frames = import_folder(join('data', 'graphics', 'player'))

    def setup(self):
        tmx_map = load_pygame(join('data', 'tmx', 'Test.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        for x, y, image in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), image, self.all_sprites)
        for x, y, image in tmx_map.get_layer_by_name('Plants and rocks').tiles():
            Sprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), image, self.all_sprites)
        
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                self.player = Player(self.player_frames, (obj.x, obj.y), self.all_sprites)
        
    def scale_to_fit(self):
        target_width, target_height = self.display_info.current_w, self.display_info.current_h
        surface_width, surface_height = self.game_surface.get_size()

        scale_x = target_width / surface_width
        scale_y = target_height / surface_height

        scale = min(scale_x, scale_y)
        new_width = int(surface_width * scale)
        new_height = int(surface_height * scale)

        scaled_surface = pygame.transform.scale(self.game_surface, (new_width, new_height))
        return scaled_surface

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

            pygame.display.update()

    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000
            
            if not self.game_started:
                self.menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_windowed_fullscreen()   

            self.all_sprites.update(dt)

            self.game_surface.fill((50, 50, 50))
            self.all_sprites.draw(self.player.rect.center)

            

            self.screen.fill((50, 50, 50))
            if self.fullscreen:
                scaled_width = int(self.display_info.current_w * self.zoom)
                scaled_height = int(self.display_info.current_h * self.zoom)
                scaled_surface = self.scale_to_fit()
                zoomed_surface = pygame.transform.scale(scaled_surface, (scaled_width, scaled_height))
                offset = ((self.display_info.current_w - scaled_width) // 2, (self.display_info.current_h - scaled_height) // 2)
                self.screen.blit(zoomed_surface, offset)

            else:
                scaled_width = int(WINDOW_WIDTH * self.zoom)
                scaled_height = int(WINDOW_HEIGHT * self.zoom)
                scaled_surface = pygame.transform.scale(self.game_surface, (scaled_width, scaled_height))
                offset = ((WINDOW_WIDTH - scaled_width) // 2, (WINDOW_HEIGHT - scaled_height) // 2)
                self.screen.blit(scaled_surface, offset)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
        
pygame.quit()