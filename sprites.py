from settings import *

class Sprite(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

class AnimatedSptrite(Sprite):

    def __init__(self, frames, pos,  groups):
        self.frame_index = 0
        self.frames = frames
        self.animation_speed = 2
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Player(AnimatedSptrite):

    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.speed = 50
        self.direction = pygame.Vector2()
        self.state = 'down'

    def input(self):
        keys = pygame.key.get_pressed()         
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt

        self.rect.y += self.direction.y * self.speed * dt

    def rotate(self):
        if self.state == 'right':
            self.image = pygame.transform.rotozoom(self.image, -90, 1)
        if self.state == 'left':
            self.image = pygame.transform.rotozoom(self.image, 90, 1)
        if self.state == 'down':
            self.image = pygame.transform.rotozoom(self.image, 180, 1)

    def animate(self, dt):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'

        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_index = self.frame_index + 5 * self.animation_speed * dt if self.direction else 0
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.rotate()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)