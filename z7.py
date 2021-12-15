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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, all_sprites, horizontal_borders, vertical_borders):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self, width, height, all_sprites):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, pos, all_sprites):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, mountain):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, mountain):
            self.rect = self.rect.move(0, 1)


def update(self):
    self.rect = self.rect.move(self.vx, self.vy)


def main():
    pygame.init()
    width = 500
    height = 500
    size = (width, height)
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    mountain = Mountain(width, height, all_sprites)
    pygame.display.set_caption("ЗА ВДВ!")
    while running:
        all_sprites.update(mountain)
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Landing(event.pos, all_sprites)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
