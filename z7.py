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


class BigBoom(pygame.sprite.Sprite):
    bombs = load_image("../data/bomb.png")
    boom = load_image("../data/boom.png")

    def __init__(self, width, height, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.width = width
        self.height = height
        self.image = BigBoom.bombs
        self.image_boom = BigBoom.boom
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0 + self.image.get_width(), width - self.image.get_width())
        self.rect.y = random.randrange(0 + self.image.get_height(), height - self.image.get_height())

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(event.pos):
            self.image = self.image_boom


def main():
    pygame.init()
    width = 500
    height = 500
    size = (width, height)
    screen = pygame.display.set_mode(size)
    running = True
    all_sprites = pygame.sprite.Group()
    pygame.display.set_caption("Boom them all")
    for i in range(20):
        BigBoom(width, height, all_sprites)
    while running:
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            all_sprites.update(event)
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
