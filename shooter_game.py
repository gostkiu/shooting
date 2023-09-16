#Створи власний Шутер!

from random import randint
from typing import Any
import pygame

HEIGHT = 600
WIDTH = 1200

SIZE = (WIDTH,HEIGHT)
FPS = 60

lost = 0
score = 0

w = pygame.display.set_mode(SIZE)
backgor = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    SIZE
)

clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

pygame.font.init()
font1 = pygame.font.Font(None,36)
font2 = pygame.font.Font(None,56)
bullets = pygame.sprite.Group()
faire_saind = pygame.mixer.Sound("fire.ogg")


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, size, speed):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(filename), 
            size
        )    
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 

    def reset(self):
        w.blit(self.image, (self.rect.x, self.rect.y))

class Playuer(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.rect.x = WIDTH
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.rect.x >= WIDTH:
                self.rect.x = 0

    def fire(self):
            new_bullet = Bullet("bullet.png",self.rect.centerx,self.rect.y,(10,35),4)
            bullets.add(new_bullet)
            faire_saind.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y = self.rect.y + self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0 
            self.rect.x = randint(10,WIDTH)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
      self.rect.y -= self.speed
      if self.rect.y < 0:
          self.kill()  





ship = Playuer("rocket.png",WIDTH/2,HEIGHT-70, (50,70),10)
enemies = pygame.sprite.Group()
enemies_num = 5
for i in range(enemies_num):
    new_enemi = Enemy("ufo.png",randint(10,WIDTH-60),0,(70,50),randint(2,6))
    enemies.add(new_enemi)

asteroids = pygame.sprite.Group()
asteroids_num = 2 
for i in range(asteroids_num):
    new_aster = Enemy("asteroid.png",randint(10,WIDTH-60),0,(70,50),2)
    asteroids.add(new_aster)


run = True
fin = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.fire()

    if not fin:
        w.blit(backgor,(0,0))
        ship.update()
        ship.reset()
        enemies.update()
        enemies.draw(w)
        asteroids.update()
        asteroids.draw(w)
        bullets.update()
        bullets.draw(w)
        text_l = font1.render("Пропущено "+ str(lost),True,(255,50,250))
        w.blit(text_l, (0,0))

        killed_enemies = pygame.sprite.groupcollide(
                        enemies,bullets,True,True
        )
        for ke in killed_enemies:
            score += 1
            new_enemi = Enemy("ufo.png",randint(10,WIDTH-60),0,(70,50),randint(2,6))
            enemies.add(new_enemi)
        text_s = font1.render("Збито "+ str(score),True,(255,50,250))
        w.blit(text_s, (0,30))

        if lost > 3 or pygame.sprite.spritecollide(ship,enemies,False) :
            text_lus = font2.render("Програв",True,(255,50,250))
            w.blit(text_lus, (WIDTH/2,HEIGHT/2))
            fin = True
        if score > 5:
            text_w = font2.render("Виграв ",True,(255,50,250))
            w.blit(text_w, (WIDTH/2,HEIGHT/2))
            fin = True





    pygame.display.update()
    clock.tick(FPS)