from settings import *

class Sprite(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

class Player(Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.speed = 500

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed * dt

    def update(self, dt):
        self.move(dt)