from settings import *

class Sprite(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.copy()

class CollidableSprite(Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

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

    def __init__(self, frames, pos, groups, collision_sprites):
        super().__init__(frames, pos, groups)
        self.speed = 50
        self.direction = pygame.Vector2()
        self.state = 'down'
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy()

    def input(self):
        keys = pygame.key.get_pressed()         
        
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.centerx += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.rect.centerx
        self.collision('horizontal')
        self.rect.centery += self.direction.y * self.speed * dt
        self.hitbox.centery = self.rect.centery
        self.collision('vertical')

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
        
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