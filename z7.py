import os
import sys
import random

import pygame


# Изображение не получится загрузить
# без предварительной инициализации pygame
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("plain1.png")

    def __init__(self, width, height, plainers, pos):
        super().__init__(plainers)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.add(plainers)
        self.mask = pygame.mask.from_surface(self.image)
        # вычисляем маску для эффективного сравнения
        # располагаем горы внизу
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Landing(pygame.sprite.Sprite):
    image = load_image("cube.png")

    def __init__(self, pos, all_sprites, plainers, height):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.height = height
        self.plainers = plainers
        self.flag = 0
        self.all_sprites = all_sprites
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *event):
        if self.rect.y > self.height:
            self.all_sprites.remove(-1)
        if self.flag == 0:
            self.rect = self.rect.move(0, 1)
        if self.plainers:
            a = pygame.sprite.spritecollide(self, self.plainers, False)
            if len(a) > 0:
                self.flag = 1
                self.rect = self.rect.move(0, 0)
        if event:
            if event[0].type == pygame.KEYDOWN:
                if event[0].key == pygame.K_LEFT:
                    self.rect.x -= 10
                    # если была нажата стрелка вправо
                if event[0].key == pygame.K_RIGHT:
                    self.rect.x += 10


def update(self):
    self.rect = self.rect.move(self.vx, self.vy)


def main():
    pygame.init()
    width = 500
    height = 500
    size = (width, height)
    screen = pygame.display.set_mode(size)
    fps = 50
    clock = pygame.time.Clock()
    running = True
    plainers = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    pygame.display.set_caption("ЗА ВДВ!")
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            all_sprites.update(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if len(all_sprites) != 1:
                    Landing(event.pos, all_sprites, plainers, height)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                Mountain(width, height, plainers, event.pos)
        clock.tick(fps)
        all_sprites.draw(screen)
        all_sprites.update()
        plainers.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
