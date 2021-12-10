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


class Car(pygame.sprite.Sprite):
    car = load_image("../data/car.png")

    def __init__(self, width, height, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Car.car
        self.image_left = self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.width = width
        self.height = height
        self.rect.y = 0
        self.flag = 0

    def update(self):
        speed = 3
        if self.rect.x == self.width - self.image.get_width():
            self.flag = 1
        elif self.rect.x == 0:
            self.flag = 0
        if self.flag == 0:
            self.image = Car.car
            self.rect.x += speed
        elif self.flag == 1:
            self.image = self.image_left
            self.rect.x -= speed


def main():
    pygame.init()
    width = 600
    height = 95
    size = (width, height)
    screen = pygame.display.set_mode(size)
    running = True
    fps = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption("Машинка")
    all_sprites = pygame.sprite.Group()
    Car(width, height, all_sprites)
    while running:
        screen.fill(pygame.Color('white'))
        all_sprites.draw(screen)
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()

