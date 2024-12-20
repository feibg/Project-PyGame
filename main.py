from settings import *
from support import *
from sprites import *
from groups import *
from button import *
import os

class Game:
    def __init__(self):
        self.display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(WINDOW_CAPTION)
        self.running = True
        self.game_running = False
        self.fullscreen = True
        self.scroll = 0
        self.scroll_speed = 5
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()

        self.load_assets()
        self.setup()

    def load_assets(self):
        self.background_images = []
        for i in range(1, 5):
            self.background_images.append(pygame.image.load(join('data', 'graphics', 'menu', f'background{i}.png')).convert_alpha())
        self.button_background = pygame.image.load(join('data', 'graphics', 'menu', 'button.png'))
        self.player_frames = import_folder(join('data', 'graphics', 'player'))
        self.lato = pygame.font.Font(join('data', 'graphics', 'font', 'Lato.ttf'), 50)

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

    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.fullscreen = not self.fullscreen

    def draw_background(self, current_w):
        for x in range(5):
            self.scroll_speed = 1
            for i in self.background_images:
                self.screen.blit(i, (x * current_w - self.scroll * self.scroll_speed, 0))
                self.scroll_speed += 1

    def menu(self):
        while self.running:
            
            current_w, current_h = pygame.display.get_surface().get_size()

            self.button_background = pygame.transform.scale(self.button_background, (300, 80))

            menu_mouse_pos = pygame.mouse.get_pos()

            if self.fullscreen:
                for i in range(0, 4):
                    self.background_images[i] = pygame.transform.scale(self.background_images[i], (self.display_info.current_w, self.display_info.current_h))
            elif not self.fullscreen:
                for i in range(0, 4):
                    self.background_images[i] = pygame.transform.scale(self.background_images[i], (WINDOW_WIDTH, WINDOW_HEIGHT))
                
            menu_text = self.lato.render('Game', True, (255, 255, 255))
            menu_rect = menu_text.get_rect(center=(current_w / 2, current_h / 2 - 200))

            play_button = Button(self.button_background, (current_w / 2, current_h / 2 - 100), 'Play', self.lato, (200, 200, 200), (255, 255, 255))
            options_button = Button(self.button_background, (current_w / 2, current_h / 2), 'Options', self.lato, (200, 200, 200), (255, 255, 255))
            quit_button = Button(self.button_background, (current_w / 2, current_h / 2 + 100), 'Quit', self.lato, (200, 200, 200), (255, 255, 255))

            self.draw_background(current_w)

            self.screen.blit(menu_text, menu_rect)

            for button in [play_button, options_button, quit_button]:
                button.change_color(menu_mouse_pos)
                button.update(self.screen)

            self.scroll += 0.5 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.input(menu_mouse_pos):
                        self.game_running = True
                        self.run()
                    if options_button.input(menu_mouse_pos):
                        pass
                    if quit_button.input(menu_mouse_pos):
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
                        self.toggle_fullscreen()   

            self.all_sprites.update(dt)

            self.screen.fill((50, 50, 50))
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.menu()
        
pygame.quit()