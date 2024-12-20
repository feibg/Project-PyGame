from settings import *
from support import *
from sprites import *
from groups import *
from button import *
import os

class Game:
    def __init__(self):
        self.fullscreen_info = pygame.display.Info()
        self.fullscreen_w, self.fullscreen_h = self.fullscreen_info.current_w, self.fullscreen_info.current_h
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.current_w, self.current_h = WINDOW_WIDTH, WINDOW_HEIGHT
        self.running = True
        self.game_running = False
        self.fullscreen = False
        self.game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.scroll = 0
        self.scroll_speed = 5
        self.clock = pygame.time.Clock()
        self.all_sprites = AllSprites(self.game_surface)
        self.collision_sprites = pygame.sprite.Group()
        self.button_offset = 75

        self.load_assets()
        self.setup()

    def load_assets(self):
        self.background_image = pygame.transform.scale(pygame.image.load(join('data', 'graphics', 'menu', 'background.png')).convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.unscaled_button_background = pygame.image.load(join('data', 'graphics', 'menu', 'button.png'))
        self.player_frames = import_folder(join('data', 'graphics', 'player'))
        self.lato = pygame.font.Font(join('data', 'graphics', 'font', 'Lato.ttf'), 50)

    def setup(self):
        tmx_map = load_pygame(join('data', 'tmx', 'Test.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        for x, y, image in tmx_map.get_layer_by_name('Ground').tiles():
            Sprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), image, self.all_sprites)
        for x, y, image in tmx_map.get_layer_by_name('Plants and rocks').tiles():
            CollidableSprite((x * tmx_map.tilewidth, y * tmx_map.tileheight), image, (self.all_sprites, self.collision_sprites))
        
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'player':
                self.player = Player(self.player_frames, (obj.x, obj.y), self.all_sprites, self.collision_sprites)

        self.scale = min(self.fullscreen_w / WINDOW_WIDTH, self.fullscreen_h / WINDOW_HEIGHT)
        self.scaled_w = int(WINDOW_WIDTH * self.scale)
        self.scaled_h = int(WINDOW_HEIGHT * self.scale)

        self.button_background = pygame.transform.scale(self.unscaled_button_background, (200, 70))

        self.play_button = Button(self.button_background, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - self.button_offset + 50), 'Play', self.lato, (200, 200, 200), (255, 255, 255))
        self.options_button = Button(self.button_background, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50), 'Options', self.lato, (200, 200, 200), (255, 255, 255))
        self.quit_button = Button(self.button_background, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + self.button_offset + 50), 'Quit', self.lato, (200, 200, 200), (255, 255, 255))

    def menu(self):
        while self.running:

            unscaled_mouse_pos = pygame.mouse.get_pos()
            if not self.fullscreen:
                mouse_pos_x = unscaled_mouse_pos[0]
                mouse_pos_y = unscaled_mouse_pos[1]
            else:
                mouse_pos_x = unscaled_mouse_pos[0] / self.scale
                mouse_pos_y = unscaled_mouse_pos[1] / self.scale

            self.screen.fill((50, 50, 50))
            self.game_surface.blit(self.background_image, (0, 0))

            for button in [self.play_button, self.options_button, self.quit_button]:
                button.change_color((mouse_pos_x, mouse_pos_y))
                button.update(self.game_surface)

            if self.fullscreen:
                scaled_surface = pygame.transform.scale(self.game_surface, (self.scaled_w, self.scaled_h))
                self.screen.blit(scaled_surface, (0, 0))
            else:
                self.screen.blit(self.game_surface, (0, 0))

            self.scroll += 0.5 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((self.fullscreen_w, self.fullscreen_h), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                        self.current_w, self.current_h = pygame.display.get_surface().get_size()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.input((mouse_pos_x, mouse_pos_y)):
                        self.game_running = True
                        self.run()
                    if self.options_button.input((mouse_pos_x, mouse_pos_y)):
                        pass
                    if self.quit_button.input((mouse_pos_x, mouse_pos_y)):
                        self.running = False


            pygame.display.update()

    def run(self):

        while self.game_running:

            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode((self.fullscreen_w, self.fullscreen_h), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                        self.current_w, self.current_h = pygame.display.get_surface().get_size()

            self.all_sprites.update(dt)

            self.screen.fill((50, 50, 50))
            self.all_sprites.draw(self.player.rect.center)

            if self.fullscreen:
                scaled_surface = pygame.transform.scale(self.game_surface, (self.scaled_w, self.scaled_h))
                self.screen.blit(scaled_surface, (0, 0))
            else:
                self.screen.blit(self.game_surface, (0, 0))
            
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.menu()
        
pygame.quit()