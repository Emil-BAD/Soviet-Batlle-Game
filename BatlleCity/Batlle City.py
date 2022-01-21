import pygame
import os
import sys
import random
import time


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс для стен
class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(walls, all_sprites)
        self.image = load_image("block.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        hardness[self] = 5


class Game_menu(pygame.sprite.Sprite):
    def __init__(self, flag):
        super().__init__(all_sprites)
        self.image = load_image('dop.png')
        self.rect = self.image.get_rect().move(
            tile_width * 20, tile_height * 0)


# для жизней в виде серпов
class Life(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lifes_group, all_sprites)
        self.image = load_image('life.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.up = load_image('UpTank.png')
        self.down = load_image('DownTank.png')
        self.right = load_image('RightTank.png')
        self.left = load_image('LeftTank.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.turn = 'up'

    def move(self, x, y, *movement):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0], tile_height * self.pos[1])
        if bot is None:
            pos = star.pos
        else:
            pos = bot.pos
        if bot2 is None:
            pos2 = star.pos
        else:
            pos2 = bot2.pos
        if movement:
            if movement[0] == "up":
                self.turn = 'up'
                self.image = self.up
                if y > 0 and level_map[y - 1][x] == ".":
                    if (self.pos[0], self.pos[1] - 1) != pos and (self.pos[0], self.pos[1] - 1) != pos2:
                        player.move(x, y - 1)
            elif movement[0] == "down":
                self.turn = 'down'
                self.image = self.down
                if y < max_y and level_map[y + 1][x] == ".":
                    if (self.pos[0], self.pos[1] + 1) != pos and (self.pos[0], self.pos[1] + 1) != pos2:
                        player.move(x, y + 1)
            elif movement[0] == "left":
                self.turn = 'left'
                self.image = self.left
                if x > 0 and level_map[y][x - 1] == ".":
                    if (self.pos[0] - 1, self.pos[1]) != pos and (self.pos[0] - 1, self.pos[1]) != pos2:
                        player.move(x - 1, y)
            elif movement[0] == "right":
                self.turn = 'right'
                self.image = self.right
                if x < max_x and level_map[y][x + 1] == ".":
                    if (self.pos[0] + 1, self.pos[1]) != pos and (self.pos[0] + 1, self.pos[1]) != pos2:
                        player.move(x + 1, y)

    # поворот танка
    def turning(self):
        if self.turn == "up":
            self.image = self.up
        elif self.turn == 'down':
            self.image = self.down
        elif self.turn == "right":
            self.image = self.right
        elif self.turn == "left":
            self.image = self.left

    def check_lifes(self):
        global flag
        if life == 2:
            l3.kill()
            if flag == 0:
                self.kill()
                flag += 1
        elif life == 1:
            l2.kill()
            if flag == 1:
                self.kill()
                flag += 1
        elif life == 0:
            l1.kill()
            if flag == 2:
                self.kill()
                lose_sc = Lose()
                flag += 1


#  снаряд нашего танка
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, turning):
        super().__init__(bullets_group, all_sprites)
        self.up = load_image('bullet_up.png')
        self.wall1 = pygame.mixer.Sound('sounds/wall1.wav')
        self.down = load_image('bullet_down.png')
        self.left = load_image('bullet_l.png')
        self.right = load_image('bullet_r.png')
        self.pos = (pos_x, pos_y)
        self.turn = turning
        self.image = self.check()
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        for i in bullets_group:
            if i.rect.x > 1000 - i.image.get_width() or i.rect.x < 0 - i.image.get_width() or i.rect.y > 1000 - i.image.get_height() or i.rect.y < 0 - i.image.get_height():
                i.kill()
        if self.turn == 'up':
            self.rect.y -= 10
        elif self.turn == 'down':
            self.rect.y += 10
        elif self.turn == 'left':
            self.rect.x -= 10
        elif self.turn == 'right':
            self.rect.x += 10
        check_insert = pygame.sprite.spritecollide(self, walls, False)
        if len(check_insert) > 0:
            hardness[check_insert[0]] = hardness[check_insert[0]] - 1
            self.wall1.play()
            self.kill()
        if bot is not None:
            check_insert_bot = pygame.sprite.collide_mask(self, bot)
            if check_insert_bot is not None:
                bot.life -= 1
                self.kill()
        if bot2 is not None:
            check_insert_bot2 = pygame.sprite.collide_mask(self, bot2)
            if check_insert_bot2 is not None:
                bot2.life -= 1
                self.kill()

    def check(self):
        if self.turn == 'up':
            return self.up
        elif self.turn == 'down':
            return self.down
        elif self.turn == 'left':
            return self.left
        elif self.turn == 'right':
            return self.right


# снаряды противников
class Bullet_bot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, turning):
        super().__init__(bullets_bot_group, all_sprites)
        self.image = load_image('bot_bullet.png')
        self.wall1 = pygame.mixer.Sound('sounds/wall1.wav')
        self.pos = (pos_x, pos_y)
        self.turn = turning
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        global life
        for i in bullets_group:
            if i.rect.x > 1000 - i.image.get_width() or i.rect.x < 0 - i.image.get_width() or i.rect.y > 1000 - i.image.get_height() or i.rect.y < 0 - i.image.get_height():
                i.kill()
        if self.turn == 'up':
            self.rect.y -= 10
        elif self.turn == 'down':
            self.rect.y += 10
        elif self.turn == 'left':
            self.rect.x -= 10
        elif self.turn == 'right':
            self.rect.x += 10
        check_insert = pygame.sprite.spritecollide(self, walls, False)
        check_insert_player = pygame.sprite.spritecollide(self, player_group, False)
        check_insert_star = pygame.sprite.spritecollide(self, star_group, False)
        if len(check_insert) > 0:
            hardness[check_insert[0]] = hardness[check_insert[0]] - 5
            self.wall1.play()
            self.kill()
        if len(check_insert_player) > 0:
            life -= 1
            self.kill()
        if len(check_insert_star) > 0:
            star.kill()
            self.kill()


# звезда - главная жизнь
class Star(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(star_group, all_sprites)
        self.image = star_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 5, tile_height * self.pos[1])


# пыль из под танка
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("dust.png")]
    for scale in (0, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, turning):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.turn = turning

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.5

    def update(self):
        # движение с ускорением под действием гравитации
        # перемещаем частицу
        if self.turn == 'up':
            self.velocity[1] += self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        if self.turn == 'down':
            self.velocity[1] -= self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        if self.turn == 'left':
            self.velocity[0] += self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        if self.turn == 'right':
            self.velocity[0] -= self.gravity
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(player.rect[0] - 10, player.rect[1] - 10, player.rect[2] + 10,
                                     player.rect[3] + 10):
            self.kill()


class Bot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bots_group, all_sprites)
        self.image = load_image("rightbot.png")
        self.up = load_image('upbot.png')
        self.down = load_image('downbot.png')
        self.right = load_image('rightbot.png')
        self.left = load_image('leftbot.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.shoot_sound = pygame.mixer.Sound('sounds/bot_shoot.wav')
        self.life = 3
        self.turn = 'right'

    def move_bot(self, target):
        next_pos = self.find_path_step(self.pos, target)
        if next_pos[0] == self.pos[0] - 1:
            self.turn = 'left'
        elif next_pos[0] == self.pos[0] + 1:
            self.turn = 'right'
        elif next_pos[1] == self.pos[1] - 1:
            self.turn = 'up'
        elif next_pos[1] == self.pos[1] + 1:
            self.turn = 'down'
        if next_pos != player.pos:
            self.pos = next_pos
            self.rect = self.image.get_rect().move(
                tile_width * self.pos[0], tile_height * self.pos[1])

    def shoting(self):
        if self.pos[0] == player.pos[0] or self.pos[1] == player.pos[1]:
            if self.pos[0] > player.pos[0]:
                self.shoot_sound.play()
                self.image = self.left
                self.turn = 'left'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
            elif self.pos[0] < player.pos[0]:
                self.shoot_sound.play()
                self.image = self.right
                self.turn = 'right'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
            elif self.pos[1] > player.pos[1]:
                self.shoot_sound.play()
                self.image = self.up
                self.turn = 'up'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
            elif self.pos[1] < player.pos[1]:
                self.shoot_sound.play()
                self.image = self.down
                self.turn = 'down'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
        elif self.pos[0] == 10 and self.pos[1] == 19:
            if self.pos[0] > star.pos[0]:
                self.shoot_sound.play()
                self.image = self.left
                self.turn = 'left'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
            elif self.pos[0] < star.pos[0]:
                self.shoot_sound.play()
                self.image = self.right
                self.turn = 'right'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
            elif self.pos[1] > star.pos[1]:
                self.shoot_sound.play()
                self.image = self.up
                self.turn = 'up'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)
            elif self.pos[1] < star.pos[1]:
                self.shoot_sound.play()
                self.image = self.down
                self.turn = 'down'
                Bullet_bot(self.pos[0], self.pos[1], self.turn)

    def turning(self):
        if self.turn == "up":
            self.image = self.up
        elif self.turn == 'down':
            self.image = self.down
        elif self.turn == "right":
            self.image = self.right
        elif self.turn == "left":
            self.image = self.left

    def check(self):
        if (self.pos[0] - 1, self.pos[1]) == player.pos:
            self.image = self.left
        elif (self.pos[0] + 1, self.pos[1]) == player.pos:
            self.image = self.right
        elif (self.pos[0], self.pos[1] - 1) == player.pos:
            self.image = self.up
        elif (self.pos[0], self.pos[1] + 1) == player.pos:
            self.image = self.down

    def check_lifes(self):
        global count, kills
        if self.life == 0:
            count += 1
            kills += 1
            self.kill()

    # посик самого короткого пути для противника
    def find_path_step(self, start, target):
        INF = 1000
        x, y = start
        distance = [[INF] * 20 for _ in range(20)]
        distance[y][x] = 0
        prev = [[None] * 20 for _ in range(20)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < 20 and 0 <= next_y < 20 and level_map[next_y][next_x] != '#' \
                        and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Lose(pygame.sprite.Sprite):
    def __init__(self):
        global lose
        super().__init__(all_sprites)
        self.image = load_image("lose.png")
        self.rect = self.image.get_rect().move(
            tile_width * 0, tile_height * -20)
        self.pos = (0, 0)
        self.running = False
        lose = True
        engine.stop()
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load("sounds/Funeral March.mp3")
        pygame.mixer.music.play(-1)
        self.clearing()

    def clearing(self):
        global bot, bot2
        bot = None
        bot2 = None
        star.kill()
        player.kill()

    def update(self):
        global los_pos
        if self.rect.y != 0:
            self.rect.y += 10
        if self.rect.y == 0:
            los_pos = self.pos


def create_particles(position, turning):
    # количество создаваемых частиц
    particle_count = 25
    # возможные скорости
    numbers = range(-3, 4)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), turning)


#  выход
def terminate():
    pygame.quit()
    sys.exit()


# начало
def start_screen():
    select_sound = pygame.mixer.Sound('sounds/menu.wav')
    enter = pygame.mixer.Sound('sounds/enter.wav')
    fon = pygame.transform.scale(load_image('start.png'), screen_size)
    titres_scr = load_image('titres.png')
    count = 1
    but_start = load_image('but_start .png')
    but_titres = load_image('but_titres .png')
    but_exit = load_image('but_exit.png')
    sel_start = load_image('select_start.png')
    sel_titres = load_image('select_titres.png')
    sel_exit = load_image('select_exit.png')
    start = sel_start
    titres = but_titres
    exiting = but_exit
    pos = 0
    flag = 0

    while True:
        if count == 1:
            start = sel_start
            titres = but_titres
            exiting = but_exit
        elif count == 2:
            start = but_start
            titres = sel_titres
            exiting = but_exit
        elif count == 3:
            start = but_start
            titres = but_titres
            exiting = sel_exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if count != 1:
                        select_sound.play()
                        count -= 1
                elif event.key == pygame.K_DOWN:
                    if count != 3:
                        select_sound.play()
                        count += 1
                if event.key == pygame.K_RETURN:
                    enter.play()
                    if count == 1:
                        pos = 1
                        return
                    elif count == 2:
                        flag = 1
                        screen.blit(titres_scr, (0, 0))
                        pos = 2
                    elif count == 3:
                        terminate()
                if pos == 2 and event.key == pygame.K_ESCAPE:
                    flag = 0
        if flag == 0:
            screen.blit(fon, (0, 0))
            screen.blit(start, (135, 400))
            screen.blit(titres, (135, 500))
            screen.blit(exiting, (135, 600))
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    try:
        filename = "maps/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError:
        print('Нет такого уровня(')


def generate_level(level):
    global spawn, spawn_bot1, spawn_bot2
    try:
        new_player, x, y = None, None, None
        star, x_star, y_star = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('empty', x, y)
                    Wall(x, y)
                elif level[y][x] == '@':
                    spawn = (x, y)
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                elif level[y][x] == "B":
                    Tile('empty', x, y)
                    spawn_bot2 = x, y
                elif level[y][x] == "A":
                    Tile('empty', x, y)
                    spawn_bot1 = x, y
                elif level[y][x] == '*':
                    Tile('empty', x, y)
                    star = Star(x, y)
                    x_star = x
                    y_star = y
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y, star, x_star, y_star
    except TypeError:
        pass


def update_walls():
    if hardness:
        for i, j in hardness.items():
            if j == 4:
                i.image = load_image('4block.png')
            if j == 3:
                i.image = load_image('2block.png')
            if j == 2:
                i.image = load_image('1block.png')
            if j == 1:
                i.image = load_image('3block.png')
            if j <= 0:
                level_map[i.rect.y // tile_height] = my_replace(i.rect.y // tile_height, i.rect.x // tile_width, '.')
                i.kill()


# замена сивола в строке
def my_replace(y, x, simvol):
    signs = list()
    string = level_map[y]
    for i in string:
        signs.append(i)
    signs[x] = simvol
    return ''.join(signs)


# создание нашего играка
def creature_player():
    global player
    if len(player_group) == 0 and life != 0 and lose is False:
        player = Player(spawn[0], spawn[1])


# создание противников
def creature_bots():
    global bot, bot2
    if bot is None and bot2 is None and count != 4 and lose is False:
        bot = Bot(spawn_bot1[0], spawn_bot1[1])
        bot2 = Bot(spawn_bot2[0], spawn_bot2[1])


# проверка разрушаемости звезды
def check_star():
    if len(star_group) == 0 and lose is False:
        Lose()


def change_levels():
    global count, lvl, kills
    if count == 4 and kills != 20:
        for i in walls:
            i.kill()
        for i in star_group:
            i.kill()
        for i in player_group:
            i.kill()
        for i in bots_group:
            i.kill()
        for i in tiles_group:
            i.kill()
        hardness.clear()
        begin(2 + lvl)
        lvl += 1
        count = 0
    if kills == 20:
        global bot, bot2, player
        bot = None
        bot2 = None
        star.kill()
        player.kill()
        wining()


# начало
def begin(num_of_level):
    global level_map, player, level_x, level_y, star, x_star, y_star
    level_map = load_level(f'level{num_of_level}.txt')
    player, level_x, level_y, star, x_star, y_star = generate_level(level_map)


# победа
def wining():
    win_scn = pygame.transform.scale(load_image('win.png'), screen_size)
    pygame.mixer.music.stop()
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load('sounds/win.mp3')
    pygame.mixer.music.play(-1)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            screen.blit(win_scn, (0, 0))
            pygame.display.flip()
            clock.tick(FPS)


def sec_func():  # таймер
    if start:
        timing = int(time.time() - startTime)
        hours = timing // 3600
        mins = (timing % 3600) // 60
        seconds = timing % 60
        hms = (f"{'0' * (2 - len(str(hours)))}{str(hours)}:{'0' * (2 - len(str(mins)))}{str(mins)}:"
               f"{'0' * (2 - len(str(seconds)))}{str(seconds)}")
        return hms


def text():
    global flag2, string_rendered, tring_rendered
    font = pygame.font.Font('fonts/Pixel.ttf', 40)
    if flag2 == 1:
        string_rendered = font.render(f'{kills}', 1, pygame.Color('white'))
        tring_rendered = font.render(f'{sec_func()}', 1, pygame.Color('white'))
        flag2 = 0
    screen.blit(string_rendered, (511, 610))
    screen.blit(tring_rendered, (926, 610))


pygame.display.set_caption("Soviet Batlle")
pygame.init()
bot = None
bot2 = None
string_rendered = None
tring_rendered = None
screen_size = width, height = 1150, 1000
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
FPS = 50
start_screen()
pygame.mixer.music.load('sounds/main_theme.mp3')
pygame.mixer.music.set_volume(0.45)
pygame.mixer.music.play(-1)
engine = pygame.mixer.Sound('sounds/engine.wav')
engine.play(-1)
player = None
spawn_bot1 = (None, None)
spawn_bot2 = (None, None)
TRACERS = []
kills = 0
# группы спрайтов
hardness = dict()
all_sprites = pygame.sprite.Group()
bots_group = pygame.sprite.Group()
walls = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tracers_group = pygame.sprite.Group()
lifes_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
bullets_bot_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()

running = True

tile_images = {"empty": load_image("pol.png")}
player_image = load_image("OurTank.png")
star_image = load_image("star.png")
bullet_image = load_image("bullet_up.png")

tile_width = tile_height = 50

BOT_EVENT_TYPE = 30
BOT_EVENT_TYPE2 = 30
PLAYER_EVENT_TYPE = 30
BOT_SHOT_TYPE = 30
BOT_SHOT_TYPE2 = 30
pygame.time.set_timer(pygame.USEREVENT, 1000)

a = 0
motor_sound = pygame.mixer.Sound("sounds/motor2.wav")
spawn = (None, None)
lose = False
life = 3
win = 0
count = 0
lvl = 0
los_pos = None, None
flag = 0
flag2 = 1
level_map = None
begin(1)
gm = Game_menu(0)
bots = list()
l1 = Life(20, 2)
l2 = Life(21, 2)
l3 = Life(22, 2)
max_x = level_x
max_y = level_y
f = 0
pygame.time.set_timer(BOT_EVENT_TYPE, 200)
pygame.time.set_timer(BOT_SHOT_TYPE, 300)
startTime = time.time()
start = True
while running:
    change_levels()
    creature_bots()
    update_walls()
    check_star()
    player.check_lifes()
    if bot is not None:
        bot.check_lifes()
        if bot.life == 0:
            bot = None
    if bot2 is not None:
        bot2.check_lifes()
        if bot2.life == 0:
            bot2 = None
    creature_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == BOT_EVENT_TYPE:
            if bot is not None:
                bot.move_bot(player.pos)
                bot.turning()
            if bot2 is not None:
                bot2.move_bot((10, 19))
                bot2.turning()
        if event.type == BOT_SHOT_TYPE:
            if bot is not None:
                bot.check()
                bot.shoting()
            if bot2 is not None:
                bot2.check()
                bot2.shoting()
        elif event.type == pygame.KEYDOWN:
            if len(player_group) > 0:
                if event.key == pygame.K_UP:
                    create_particles((player.rect.x, player.rect.y), "up")
                    player.move(player.pos[0], player.pos[1], "up")
                elif event.key == pygame.K_DOWN:
                    create_particles((player.rect.x, player.rect.y), "down")
                    player.move(player.pos[0], player.pos[1], "down")
                elif event.key == pygame.K_LEFT:
                    create_particles((player.rect.x, player.rect.y), "left")
                    player.move(player.pos[0], player.pos[1], "left")
                elif event.key == pygame.K_RIGHT:
                    create_particles((player.rect.x, player.rect.y), "right")
                    player.move(player.pos[0], player.pos[1], "right")
                if event.key == pygame.K_SPACE:
                    if len(bullets_group) < 1:
                        shoot = pygame.mixer.Sound('sounds/shoot.wav')
                        shoot.play()
                        bull = Bullet(player.pos[0], player.pos[1], player.turn)
    all_sprites.update()
    screen.fill(pygame.Color("black"))
    tiles_group.draw(screen)
    tracers_group.draw(screen)
    all_sprites.draw(screen)
    bullets_group.draw(screen)
    player_group.draw(screen)
    star_group.draw(screen)
    if los_pos[1] == 0:
        text()
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
