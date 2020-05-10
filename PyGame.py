import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_ESCAPE,
    KEYDOWN,
    QUIT)



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        
        super(Player, self).__init__()
        
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        
        ### PLAYER MOVEMENT
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)  ### MOVE IN PLACE FUNCTION
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        ### KEEP PLAYER ON SCREEN
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('images/missile.png').convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                ### ENEMY STARTS SLIGHTLY OFF SCREEN ON THE RIGHT
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),#RANDOMLY BETWEEN TOP AND BOTTOM OF SCREEN
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5,20) # Changed from 5, 20

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()

        self.surf = pygame.image.load('images/cloud.png').convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
                center =  (
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT) 
                )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) ### 0.25 seconds
ADDCLOUD = pygame.USEREVENT + 2 
pygame.time.set_timer(ADDCLOUD, 1000) ### 1 second

player = Player()

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

### SOUND SOURCE : Chris Bailey artistname Tripnet
### License: https://creativecommons.org/licenses/by/3.0/

pygame.mixer.music.load('sound/Sky_dodge_theme.ogg')
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.4)

move_up_sound = pygame.mixer.Sound('sound/Jet_up.ogg')
move_down_sound = pygame.mixer.Sound('sound/Jet_down.ogg')
collision_sound = pygame.mixer.Sound('sound/Boom.ogg')

move_up_sound.set_volume(0.8)
move_down_sound.set_volume(0.8)
collision_sound.set_volume(1.0)

running = True

while running:

    for event in pygame.event.get():
        
        if event.type == KEYDOWN:

        ### CHECK IF QUIT
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    clouds.update()

    screen.fill((135,206,250)) ### SKY BLUE

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        move_up_sound.stop()
        move_down_sound.stop()
        pygame.time.delay(50) ## 0.05 seconds
        
        collision_sound.play()
        pygame.time.delay(500)
        
        running = False
    
    pygame.display.flip()

    clock.tick(30) ### ticks per frame

pygame.mixer.music.stop()
pygame.mixer.quit()





