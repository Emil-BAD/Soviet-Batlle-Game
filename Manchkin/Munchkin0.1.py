import sys
import time
import random
import sqlite3
from pygame import mixer
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

door = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 51, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 81, 82, 83, 84, 85, 86,
        87]  # список для id дверей

treasure = [1, 7, 11, 12, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
            42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 68, 69,
            71, 72, 73, 75]  # список для id сокровищ

signal = 0  # сигнал для нескольких классов


class First(QMainWindow):  # Экран приветсвия
    def __init__(self):  # иницилизация
        super(QMainWindow, self).__init__()
        uic.loadUi('first.ui', self)  # загрузка макета
        self.flag = 0  # flag
        self.init_handlers()  # flag

    def init_handlers(self):  # обработка
        mixer.init()  # подключение музыки
        mixer.music.load("Music_First/mix_39m07s (audio-joiner.com).mp3")  # файл с музыкой
        mixer.music.play()  # играть музыку
        self.start.clicked.connect(self.show_main)  # подключение кнопки
        self.sound.clicked.connect(self.on_off_sound)  # подключение кнопки

    def on_off_sound(self):  # кнопка включения и выключения музыки
        if self.flag == 0:
            mixer.music.set_volume(0)
            self.flag = 1
            self.sound.setIcon(QIcon('Images/no_sound.png'))
        else:
            mixer.music.set_volume(100)
            self.flag = 0
            self.sound.setIcon(QIcon('Images/sound.png'))

    def show_main(self):  # открываем основное окно
        self.m = Main()
        self.m.show()
        self.close()  # закрваем окно приветсвия,что было по красоте


class Chooser(QMainWindow):  # класс для разложения карт вначале
    def __init__(self, signal, numbers_tresures):  # принимает сигнал и кол-во сокровищ для второго запуска
        super(Chooser, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi("choisecards.ui", self)  # загрузка макета
        self.chs = [self.ch_1, self.ch_2, self.ch_3, self.ch_4, self.ch_5, self.ch_6, self.ch_7,
                    self.ch_8]  # список обьектов qlabel для размещения карт в Choser
        self.numbers_tresures = numbers_tresures
        self.signal = signal
        self.id_treasures = list()  # список для всех сокровищ
        self.num_1, self.num_2, self.num_3, self.num_4, self.num_5, self.num_6, self.num_7, self.num_8 = \
            0, 0, 0, 0, 0, 0, 0, 0
        self.list_of_chosedcard = list()
        self.take.clicked.connect(self.taker)  # подключение кнопки
        self.initer()  # запуск функции

    def initer(self):  # фунция для не заполнения иниц.
        if self.signal == 0:  # сигнал для разделение Choser
            self.take.hide()  # скрывает кнопку для первого открытия
            self.num_1 = random.choice(treasure)  # выбрать рандомное id для открытия двери
            self.id_treasures.append(self.num_1)  # добавляет id в общий список с сокровищам
            pixmap_1 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_1)}).jpg"  # берёт нужное изображение
            )
            self.ch_1.installEventFilter(self)  # фильтр для сканирования нажатия мышкой по qlabel
            self.ch_1.setPixmap(pixmap_1)  # ставит то изображение
            treasure.remove(self.num_1)  # удаление из общего списка выпавшей карты
            self.num_2 = random.choice(treasure)
            self.id_treasures.append(self.num_2)
            pixmap_2 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_2)}).jpg"
            )
            self.ch_2.setPixmap(pixmap_2)
            self.ch_2.installEventFilter(self)
            treasure.remove(self.num_2)
            self.num_3 = random.choice(treasure)
            self.id_treasures.append(self.num_3)
            pixmap_3 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_3)}).jpg"
            )
            self.ch_3.setPixmap(pixmap_3)
            self.ch_3.installEventFilter(self)
            treasure.remove(self.num_3)
            self.num_4 = random.choice(treasure)
            self.id_treasures.append(self.num_4)
            pixmap_4 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_4)}).jpg"
            )
            self.ch_4.setPixmap(pixmap_4)
            self.ch_4.installEventFilter(self)
            treasure.remove(self.num_4)
            self.num_5 = random.choice(treasure)
            self.id_treasures.append(self.num_5)
            pixmap_5 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_5)}).jpg"
            )
            self.ch_5.setPixmap(pixmap_5)
            self.ch_5.installEventFilter(self)
            treasure.remove(self.num_5)
            self.num_6 = random.choice(treasure)
            self.id_treasures.append(self.num_6)
            pixmap_6 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_6)}).jpg"
            )
            self.ch_6.setPixmap(pixmap_6)
            self.ch_6.installEventFilter(self)
            treasure.remove(self.num_6)
            self.num_7 = random.choice(treasure)
            self.id_treasures.append(self.num_7)
            pixmap_7 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_7)}).jpg"
            )
            self.ch_7.setPixmap(pixmap_7)
            self.ch_7.installEventFilter(self)
            treasure.remove(self.num_7)
            self.num_8 = random.choice(treasure)
            self.id_treasures.append(self.num_8)
            pixmap_8 = QPixmap(
                f"Images/Treasures/treasures ({str(self.num_8)}).jpg"
            )
            self.ch_8.setPixmap(pixmap_8)
            self.ch_8.installEventFilter(self)
            treasure.remove(self.num_8)
        else:
            self.take.show()
            for card in range(self.numbers_tresures):
                num = random.choice(treasure)
                self.id_treasures.append(num)
                pixmap = QPixmap(
                    f"Images/Treasures/treasures ({str(num)}).jpg"
                )
                self.chs[card].setPixmap(pixmap)
                self.chs[card].installEventFilter(self)
                treasure.remove(num)

    def eventFilter(self, source, event):  # принимает нажатие мыши на qlabel
        if self.signal == 0:  # сигнал для разделения
            if event.type() == QtCore.QEvent.MouseButtonPress:  # принимает нажатие мыши на qlabel
                if source.objectName() in self.list_of_chosedcard:  # проверка обьекта на дубликат
                    self.add_check.setText(f"Данная карта уже добавлена")
                else:
                    self.list_of_chosedcard.append(source.objectName())  # основной рабочий список
                    self.add_check.setText(f"{source.objectName()[-1]}-я карта будет добавлена в руку")
                if len(self.list_of_chosedcard) == 5:  # при достижении 5 карт
                    main_window = Main()  # открывать осоновное окно
                    main_window.give_list(self.list_of_chosedcard, self.id_treasures, 0)
                    # открывать функцию принятия осоновного окна
                    Chooser.close(self)  # закрыть Choser
            return super(Chooser, self).eventFilter(source, event)
        else:  # второе открытие
            self.com.setText('Выберите сокровища')  # com - командная строка для вывода информации и текста
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if source.objectName() in self.list_of_chosedcard:
                    self.add_check.setText(f"Данная карта уже добавлена")
                else:
                    self.list_of_chosedcard.append(source.objectName())
                    self.add_check.setText(f"{source.objectName()[-1]}-я карта будет добавлена в руку")
            return super(Chooser, self).eventFilter(source, event)

    def check_event(self):  # функция для второго открытия
        global signal
        signal = 3
        listick = list()  # список для второго открытия
        for elem in range(len(self.list_of_chosedcard)):
            listick.append(self.id_treasures[int(self.list_of_chosedcard[elem][-1]) - 1])
        return 1, listick

    def taker(self):  # кнопка взять
        self.check_event()  # вызов функции
        self.close()  # второе закрытие Choser


id_doors = list()  # глобальные списки для дверей
id_treasures = list()  # для сокровищ
race = 'human'
class_mun = None


# Главный экран
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('manchkin.ui', self)  # загрузка макета
        self.timer = QtCore.QTimer()
        self.startTime = time.time()
        self.old_foot = None
        self.old_damage = None
        self.old_damage1 = None
        self.old_buff = None
        self.old_damage2 = None
        self.hands = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]
        self.num_from_cube = None
        self.res_way = None
        self.type_card = None
        self.type_door = None
        self.signal_for_cheker = None
        self.hands_panel = self.hands
        self.dialog = BigCardThing()
        self.big_doors = None
        self.chose = None
        self.things = [self.thing_1, self.thing_2, self.thing_3, self.thing_4, self.thing_5]
        self.two_hands_old_damage = None
        self.signal = False
        self.flag = True
        self.start = True
        self.damager_of_hands = list()
        self.id_treasures = list()
        self.timers = list()
        self.sbros = list()
        self.pixmap_by_filename = dict()
        self.pixmap_by_litle_thing = dict()
        self.list_of_chosedcard = set()
        self.hms = 0
        self.flag2 = 0
        self.escape = 0
        self.initer()

    def initer(self):
        self.show_choiser(0, None)
        self.timer.timeout.connect(self.sec_func)
        self.eding.hide()
        self.timer.start(1000)
        self.cub.hide()
        self.next_step.clicked.connect(self.step)
        self.updating.clicked.connect(self.updater)

    def updater(self):  # выловитель ошибок для cheker()
        self.com.setText(' ')
        try:
            self.cheker()  # вызов функции
        except Exception:
            pass

    def change_damage(self, value):  # изменение атаки
        self.old_damage = value
        self.damager.setText(str(int(self.damager.text()) + int(value)))  # считывает с макета цифру

    def minus_damage(self):  # вычетание атаки
        self.damager.setText(str(int(self.damager.text()) - int(self.old_damage)))

    def change_escape(self, buff):  # изменение значения для смывки
        self.escape += int(buff)

    def minus_escape(self):  # вычитание смывки
        self.escape -= int(self.old_escape)

    def put_hand(self, idd, buff):  # надеть в 1 руку
        if self.left_hand.pixmap() is None:  # если не заполнено, то сразу надеть
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.left_hand.setPixmap(pixmap)
            self.change_damage(buff)
            self.old_damage1 = buff
        elif self.left_hand.pixmap() is not None and self.right_hand.pixmap() is None:
            # если 1 рука занята, надеть на другую
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.right_hand.setPixmap(pixmap)
            self.change_damage(buff)
            self.old_damage2 = buff
        elif self.left_hand.pixmap() is not None and self.right_hand.pixmap() is not None:
            # если обе, убрать 1 руку,а потом надеть
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.left_hand.setPixmap(pixmap)
            self.change_damage(buff)
            self.minus_damage_for_hands(self.old_damage1)
            self.com.setText('Карта была надета на первую занятую руку')

    def put_big_thing(self, idd, buff):  # надеть большую шмотку
        if self.place_big_thing.pixmap() is None:  # если место не зянято, то надеть сразу
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.place_big_thing.setPixmap(pixmap)
            self.change_damage(buff)
        else:  # если занято, то снять лишние,убрать значение его атаки и поставить новое со значением
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.place_big_thing.setPixmap(pixmap)
            self.change_damage(buff)
            self.minus_damage()
            self.com.setText('Выбросили большую и снова взяли большую? ГЕНИЙ')

    def big_thing_check(self, idd, buff, class_or_race, obj):  # проверка большой шмотки на рассу и класс
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            self.put_big_thing(idd, buff)
            obj.clear()  # очистить место карты
            obj.hide()  # скрыть место карты
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')

    def one_hand(self, idd, buff, c_or_r, obj):
        # функция для одной руки.Принимает id, бонус от шмотки, рассу или класс, обьект для скрыти и очистки
        if c_or_r is None or c_or_r == race or c_or_r == class_mun:  # проверка
            self.put_hand(idd, buff)  # вызов функции
            obj.hide()
            obj.clear()
            if self.two_hands.pixmap() is not None:
                self.minus_damage_for_hands(self.two_hands_old_damage)
                self.two_hands.setText('2 руки')
                self.com.setText('Испарилось(')
            if len(self.damager_of_hands) == 2:  # проверка бонусов от 2 рук
                self.damager_of_hands.pop(0)
                self.damager_of_hands.insert(0, buff)
            else:
                self.damager_of_hands.append(buff)  # при снятии с рук
        else:
            self.com.setText(f'Для использования вы не {c_or_r}')

    def change_lvl(self, obj):  # для карты уровней, изменение уровня
        self.num_lvl.setText(str(int(self.num_lvl.text()) + 1))
        obj.hide()
        obj.clear()

    def minus_damage_for_hands(self, buff):  # изменение атаки более лёгким способом
        self.damager.setText(str(int(self.damager.text()) - int(buff)))

    def two_hands_check(self, idd, buff, class_or_race, obj):  # проверка расу и класс
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            self.put_two_hands(idd, buff, class_or_race)
            self.two_hands_old_damage = buff
            obj.clear()
            obj.hide()
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')
        pass

    def put_two_hands(self, idd, buff, class_or_race):  # надевание в 2 руки
        if self.two_hands.pixmap() is None and self.left_hand.pixmap() is None and self.right_hand.pixmap() is None:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.two_hands.setPixmap(pixmap)
            self.change_damage(buff)
        elif self.two_hands.pixmap() is not None:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.two_hands.setPixmap(pixmap)
            self.change_damage(buff)
            self.minus_damage()
            self.com.setText('Старая шмотка сломалась, решили поставить новую')
        elif self.two_hands.pixmap() is None and self.left_hand.pixmap() is not None and self.right_hand.pixmap() \
                is not None:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.two_hands.setPixmap(pixmap)
            self.change_damage(buff)
            [self.minus_damage_for_hands(elem) for elem in self.damager_of_hands]
            self.left_hand.setText('Левая\nрука')
            self.right_hand.setText('Правая\nрука')
            self.com.setText('Вы решили просто выбросить одноручное оружие и взять двуручное')
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')

    def heding(self, idd, buff, obj):  # надевание головняка
        if self.head.pixmap() is None:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.head.setPixmap(pixmap)
            self.old_buff = buff
            obj.clear()
            obj.hide()
        elif self.head.pixmap() is not None:
            self.minus_damage_for_hands(self.old_buff)
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.head.setPixmap(pixmap)
            obj.clear()
            obj.hide()
            self.old_buff = buff

    def header(self, idd, buff, class_or_race, obj):  # проверка на расу и класс головняка
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            self.heding(idd, buff, obj)
            self.change_damage(buff)
            obj.clear()
            obj.hide()
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')

    def doppleganger(self, obj):  # карта
        self.damager.setText(str(int(self.damager.text()) * 2))
        obj.clear()
        obj.hide()

    def cheker(self):  # проверка возвращений значений из других классов для каких-либо функций
        global signal

        if signal == 1:  # сигнал для разделения
            self.type_card, idd, buff, obj, class_or_race = self.dialog.checking_conditions_tr()
            if self.type_card == 1:
                self.little_thing(idd, buff, class_or_race, obj)
            elif self.type_card == 2:
                self.change_damage(buff)
                obj.clear()
                obj.hide()
            elif self.type_card == 3:
                self.put_on_armor(idd, buff, class_or_race, obj)
            elif self.type_card == 6:
                self.one_hand(idd, buff, class_or_race, obj)
            elif self.type_card == 7:
                self.big_thing_check(idd, buff, class_or_race, obj)
            elif self.type_card == 8:
                self.change_lvl(obj)
                self.change_damage(1)
            elif self.type_card == 9:
                self.two_hands_check(idd, buff, class_or_race, obj)
            elif self.type_card == 10:
                self.header(idd, buff, class_or_race, obj)
            elif self.type_card == 11:
                self.doppleganger(obj)
            elif self.type_card == 12:
                self.foot_bonus_check(idd, buff, class_or_race, obj)
            elif self.type_card == 13:
                self.foot_escape_check(idd, buff, class_or_race, obj)
        elif signal == 2:
            self.type_card, idd, thing, num_of_treasures = self.big_doors.fight_or_run()
            if self.type_card == 1:
                self.num_lvl.setText(str(int(self.num_lvl.text()) + 1))
                self.open_door()
                self.chose = Chooser(1, int(num_of_treasures))
                self.chose.show()
            elif self.type_card == 2:
                self.open_door()
                self.com.setText('Вы успешно смылись')
            elif self.type_card == 0:  # значение проигрыша
                hands = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]
                [elem.hide() for elem in hands]
                self.res.hide()
                self.doors.hide()
                self.treasures.hide()
                self.updating.hide()
                self.next_step.hide()
                self.eding.show()
                self.start = False
                self.eding.setText(f'ВЫ МЕРТВЫ И ПРОИГРАЛИ\nВАШЕ ВРЕМЯ: {self.sec.text()}')
        elif signal == 3:
            self.type_card, idds = self.chose.check_event()
            if int(self.type_card) == 1:
                self.give_treasures(idds)

    def foot_bonus_check(self, idd, buff, class_or_race, obj):  # проверка на расу и класс ботинок
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            self.foot_bonus(idd, buff, obj)
            self.change_damage(buff)
            obj.clear()
            obj.hide()
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')

    def foot_bonus(self, idd, buff, obj):  # само надевание ботинок с проверкой
        if self.place_foot.pixmap() is None:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.place_foot.setPixmap(pixmap)
            self.old_foot = buff
            obj.clear()
            obj.hide()
        elif self.place_foot.pixmap() is not None:
            self.minus_damage_for_hands(self.old_foot)
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.place_foot.setPixmap(pixmap)
            self.com.setText('Ой, растворились :)')
            obj.clear()
            obj.hide()
            self.old_foot = buff

    def foot_escape_check(self, idd, buff, class_or_race, obj):  # проверка ботинок
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            self.foot_escape(idd, buff, obj)
            self.change_damage(buff)
            obj.clear()
            obj.hide()
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')

    def foot_escape(self, idd, buff, obj):  # надевание ботинок
        if self.place_foot.pixmap() is None:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.place_foot.setPixmap(pixmap)
            self.escape += int(buff)
        elif self.place_foot.pixmap() is not None:
            self.minus_damage_for_hands(self.old_foot)
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
            self.place_foot.setPixmap(pixmap)
            self.escape += buff
            self.com.setText('Ой, исчезли XD')

    def little_thing(self, idd, buff, class_or_race, obj):  # проверка и надевание маленькиз шмоток
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            way = f"Images/Treasures/treasures ({str(idd)}).jpg"
            pixmap = QPixmap(way)
            self.pixmap_by_litle_thing[self.things[0]] = way
            self.things[0].setPixmap(pixmap)
            self.things.pop(0)
            self.change_damage(buff)
            obj.clear()
            obj.hide()
        elif class_or_race == 'not_wizzard' and class_mun != 'wizzard' or class_or_race == 'not_theif' \
                and class_mun != 'theif':
            way = f"Images/Treasures/treasures ({str(idd)}).jpg"
            pixmap = QPixmap(way)
            self.pixmap_by_litle_thing[self.things[0]] = way
            self.things[0].setPixmap(pixmap)
            self.things.pop(0)
            self.change_damage(buff)
            obj.clear()
            obj.hide()
        else:
            self.com.setText(f'Для использования вы {class_or_race}')

    def put_on_armor(self, idd, buff, class_or_race, obj):
        if class_or_race is None or class_or_race == race or class_or_race == class_mun:
            if self.armor.pixmap() is None:
                pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
                self.armor.setPixmap(pixmap)
                self.change_damage(buff)
            elif self.armor.pixmap() is not None:
                pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
                self.armor.setPixmap(pixmap)
                self.minus_damage()
                self.com.setText()
                self.change_damage(buff)
                self.com.setText('Старый броник пришлось выкинуть')
            obj.clear()
            obj.hide()
        elif class_or_race == 'not_wizzard' and class_mun != 'wizzard' or class_or_race == 'not_thief' \
                and class_mun != 'theif':
            if self.armor.pixmap() is None:
                pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
                self.armor.setPixmap(pixmap)
                self.change_damage(buff)
            elif self.armor.pixmap() is not None:
                pixmap = QPixmap(f"Images/Treasures/treasures ({str(idd)}).jpg")
                self.armor.setPixmap(pixmap)
                self.minus_damage()
                self.com.setText()
                self.change_damage(buff)
                self.com.setText('Старый броник пришлось выкинуть')
            obj.clear()
            obj.hide()
        else:
            self.com.setText(f'Для использования вы не {class_or_race}')

    def give_list(self, list_of_chosedcard, id_treasures1, signal):  # принимает значени из Choser
        if signal == 0:
            for elem in list_of_chosedcard:
                global id_treasures
                id_treasures.append(id_treasures1[int(elem[-1]) - 1])

    def step(self):  # ход
        if self.flag is True:
            self.open_door()
            self.cub.clicked.connect(self.cube_numbers)  # подключение кнопки
            self.res.clicked.connect(self.info_doors)
            self.func_hand()
            self.connection()
            self.flag = 2
        elif self.flag == 2:
            if int(self.num_lvl.text()) >= 10:
                hands = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]
                [elem.hide() for elem in hands]
                self.res.hide()  # скрываем всё не нужное
                self.doors.hide()
                self.treasures.hide()
                self.updating.hide()
                self.next_step.hide()
                self.start = False
                self.eding.show()
                self.eding.setText(f'ВЫ ПОБЕДИЛИ УРАА!!!\nВАШЕ ВРЕМЯ: {self.sec.text()}')
            else:
                res = self.open_door_db(self.res_way)
                if res[3] != 'monster':  # проверка что-бы монстров не пропускали
                    self.open_door()
                else:
                    self.com.setText('Беги или бейся')
            pass

    def connection(self):  # подключение для eventfilter
        self.hand1.installEventFilter(self)
        self.hand2.installEventFilter(self)
        self.hand3.installEventFilter(self)
        self.hand4.installEventFilter(self)
        self.hand5.installEventFilter(self)
        self.hand6.installEventFilter(self)

    def convert_to_binary_data(self, filename):  # функция для конвертирования изображения в байты
        try:
            with open(filename, 'rb') as file:  # принимает имя файла
                blob_data = file.read()
            return blob_data  # возвращает байты
        except TypeError:
            self.com.setText('Не верное имя файла')
            return None

    def give_treasures(self, idds):  # распределение сокровищ
        hands = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]
        for num in range(len(hands)):
            hands[num].show()
            if len(idds) > 0:
                if hands[num].pixmap() is None:
                    way = f"Images/Treasures/treasures ({str(idds[0])}).jpg"
                    pixmap = QPixmap(way)
                    hands[num].setPixmap(pixmap)
                    idds.pop(0)
                    self.pixmap_by_filename[hands[num].objectName()] = way
                else:
                    self.com.setText(
                        'Вы не уследили за своими руками, очень глупый поступок\nпоэтому теряете сокровища')

    def open_treasure_db(self, value):  # открывает базу данных сокровищ
        try:
            blob = self.convert_to_binary_data(value)  # берёт конвертированное значение
            con = sqlite3.connect('treasure.db')
            cur = con.cursor()
            result = cur.execute(
                """SELECT * FROM new_employee WHERE photo = ?""", (blob,)).fetchall()  # сравнение и сортировка
            con.close()
            self.type_door = result[0][3]
            return result[0]
        except IndexError:
            return None

    def open_door_db(self, value):  # тоже самое что и с сокровищами
        try:
            blob = self.convert_to_binary_data(value)
            con = sqlite3.connect('sqlite_python.db')
            cur = con.cursor()
            result = cur.execute(
                """SELECT * FROM new_employee WHERE photo = ?""", (blob,)).fetchall()
            con.close()
            return result[0]
        except IndexError:
            return None

    def eventFilter(self, source, event):  # для зафиксирования нажатия по Qlabel
        global signal
        if event.type() == QtCore.QEvent.MouseButtonPress:
            value = self.pixmap_by_filename[source.objectName()]
            if None == self.open_treasure_db(value):
                idd = self.open_door_db(value)
                self.dialog.processing_info(idd, 0, source)
                signal = 1
            else:
                idd = self.open_treasure_db(value)
                self.dialog.processing_info(idd, 1, source)
                signal = 1
            self.dialog.show()
        return super(Main, self).eventFilter(source, event)

    def func_hand(self):
        hands = self.hands
        for elem in range(len(id_treasures)):
            way = f"Images/Treasures/treasures ({str(id_treasures[elem])}).jpg"
            pixmap_t = QPixmap(way)
            hands[0].setPixmap(pixmap_t)
            self.pixmap_by_filename[hands[0].objectName()] = way
            hands.pop(0)
        if len(id_doors) > 1:
            for elem in range(len(id_doors)):
                way = f"Images/Monsters/monster ({str(id_doors[elem])}).jpg"
                pixmap_d = QPixmap(way)
                hands[elem].setPixmap(pixmap_d)
                self.pixmap_by_filename[hands[elem].objectName()] = way
        elif len(id_doors) == 1:
            for elem in range(len(id_doors)):
                way = f"Images/Monsters/monster ({str(id_doors[0])}).jpg"
                pixmap_d = QPixmap(way)
                hands[-1].setPixmap(pixmap_d)
                self.pixmap_by_filename[hands[-1].objectName()] = way

    def show_choiser(self, signal, numbers_tresures):  # вызов второго открытия Choser
        self.ch = Chooser(signal, numbers_tresures)
        self.ch.show()

    def open_door(self):  # открыть дверь
        try:
            idd = random.choice(door)
            way = f"Images/Monsters/monster ({str(idd)}).jpg"
            self.res_way = way  # сохранения пути для открытия БД
            self.res.setIcon(QIcon(way))
            self.res.setIconSize(QtCore.QSize(231, 291))
            door.remove(idd)
            self.sbros.append(idd)
        except IndexError:
            self.error_fun()

    def info_doors(self):  # передача в др.класс
        global signal
        signal = 2
        self.cub.show()
        h = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]
        info = self.open_door_db(self.res_way)
        if info is not None:
            self.big_doors = BigCardDoor(info, self.res, self.pixmap_by_filename, h, int(self.damager.text()),
                                         self.num_from_cube, self.place_race, self.place_class, self.com)
            self.big_doors.show()
        else:
            self.com.setText('Вы не нажали на кнопку открытия дверей, исправтесь')

    def error_fun(self):  # когда кончиться колода
        self.start = False
        self.com.setText("Увы, но все карты в колоде кончились и вы проиграли")
        self.timers.append(self.hms)

    def cube_numbers(self):  # функция имитирущая кости
        random_num = random.randint(1, 6)  # берем рандомные числа от 1 до 6
        self.number_of_cub.setText(str(random_num + self.escape))  # выводим это рандомное число с бонусом от вещей
        self.num_from_cube = random_num  # возвращаем число для дальнейшей работы с ним

    def sec_func(self):  # таймер
        if self.start:
            timing = int(time.time() - self.startTime)
            hours = timing // 3600
            mins = (timing % 3600) // 60
            seconds = timing % 60
            self.hms = (f"{'0' * (2 - len(str(hours)))}{str(hours)}:{'0' * (2 - len(str(mins)))}{str(mins)}:"
                        f"{'0' * (2 - len(str(seconds)))}{str(seconds)}")
            self.sec.setText(self.hms)


class BigCardThing(QDialog):  # использование сокровищ в руке
    def __init__(self):
        super(BigCardThing, self).__init__()
        uic.loadUi("big_dialog.ui", self)
        self.flag = None
        self.info = None
        self.id_card = None
        self.name = None
        self.image = None
        self.type_card = None
        self.m = None
        self.gold = None
        self.buf = None  # бонус от карт
        self.lvl_d = None
        self.treasure = None
        self.image = None
        self.nameobj = None
        self.class_or_race = None
        self.droper = list()
        self.initUI()

    def initUI(self):
        self.use.clicked.connect(self.checking_conditions_tr)
        self.drop.clicked.connect(self.dropping)

    def dropping(self):
        self.droper.append(self.id_card)
        self.nameobj.setText(' ')
        self.nameobj.hide()
        self.close()

    def processing_info(self, info, info_d, obj):  # сортировка информации в пременные данного класса
        self.nameobj = obj
        if info_d == 0:
            self.flag = 2
            self.info = info
            self.id_card, self.name, self.image, self.type_card, self.treasure, self.lvl_d = self.info[0], self.info[
                1], self.info[2], self.info[3], self.info[4], self.info[5]
        else:
            self.flag = 1
            self.info = info
            self.id_card, self.name, self.image, self.type_card, self.gold, self.buf, self.class_or_race = \
                self.info[0], self.info[1], self.info[2], self.info[3], self.info[4], self.info[5], self.info[6]
        self.show_card()

    def checking_conditions_tr(self):  # проверка по картам и дальнейшая передача переменных в основной класс
        if self.type_card == 'thing' and self.buf.find("bonus") != -1:
            self.close()
            return 1, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.type_card == 'potion' and self.buf.find("bonus") != -1:
            self.close()
            return 2, self.id_card, self.buf[1], self.nameobj, 0
        elif self.type_card == 'armor' and self.buf.find("bonus") != -1:
            self.close()
            return 3, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.type_card == 'one_hand' and self.buf.find("bonus") != -1:
            self.close()
            return 6, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.type_card == 'big_thing' and self.buf.find("bonus") != -1:
            self.close()
            return 7, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.type_card == 'lvl':
            self.close()
            return 8, self.id_card, 0, self.nameobj, 0
        elif self.type_card == 'two_hands':
            self.close()
            return 9, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.type_card == 'head':
            self.close()
            return 10, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.id_card == 15:
            self.close()
            return 11, self.id_card, 0, self.nameobj, 0
        elif self.type_card == 'foot' and self.buf.find("bonus") != -1:
            self.close()
            return 12, self.id_card, self.buf[1], self.nameobj, self.class_or_race
        elif self.type_card == 'foot' and self.buf.find("escape") != -1:
            self.close()
            return 13, self.id_card, self.buf[1], self.nameobj, self.class_or_race

    def show_card(self):
        if self.flag == 1:
            pixmap = QPixmap(f"Images/Treasures/treasures ({str(self.id_card)}).jpg")
            self.res.setPixmap(pixmap)
        elif self.flag == 2:
            pixmap = QPixmap(f"Images/Monsters/monster ({str(self.id_card)}).jpg")
            self.res.setPixmap(pixmap)
        pass


class BigCardDoor(QDialog):  # использование карт дверей
    def __init__(self, info, obj, pixmap_by_filename, hands, damage, escape, place_race, place_class, command_string):
        super(BigCardDoor, self).__init__()
        uic.loadUi("big_doors.ui", self)
        self.dict_pixmap = pixmap_by_filename
        self.obj = obj
        self.command_string = command_string
        self.damage = damage
        self.escape = escape
        self.hands_p = hands
        self.place_race = place_race
        self.place_class = place_class
        self.info = info
        self.id_card, self.name, self.image, self.type_card, self.treasure, self.lvl_d = self.info[0], self.info[
            1], self.info[2], self.info[3], self.info[4], self.info[5]
        self.type_c, self.idd, self.thing, self.num_treasures = None, None, None, None
        self.show_card()
        self.checking()

    def checking(self):  # скрытие и открытие кнопок для определённых карт
        if self.type_card == 'class' or self.type_card == 'class ':
            self.runing.hide()
            self.take.show()
            self.drop.show()
            self.take.clicked.connect(self.taker_for_class)
            self.fight.hide()
        elif self.type_card == 'race' or self.type_card == 'race ':
            self.runing.hide()
            self.take.show()
            self.drop.show()
            self.take.clicked.connect(self.taker_for_race)
            self.fight.hide()
        elif self.type_card == 'monster':
            self.take.hide()
            self.drop.hide()
            self.runing.show()
            self.fight.clicked.connect(self.fight_monster)
            self.runing.clicked.connect(self.escaping)
            self.fight.show()

    def taker(self):  # функция взятия
        for elem in self.hands_p:
            elem.show()
            if elem.pixmap() is None:
                way = f"Images/Monsters/monster ({str(self.id_card)}).jpg"
                elem.setPixmap(QPixmap(way))
                self.dict_pixmap[elem.objectName()] = way
                self.close()
                break
            else:
                self.com.setText("Сбросте карту с руки, что бы взять эту")

    def taker_for_class(self):  # функция взяти карт класса
        global race, class_mun

        if self.place_class.pixmap() is None:
            pixmap = QPixmap(f"Images/Monsters/monster ({str(self.id_card)}).jpg")
            self.place_class.setPixmap(pixmap)
            if self.name[-1].isdigit():
                class_mun = self.name[:-1]
            else:
                class_mun = self.name
            self.close()
        else:
            self.command_string.setText('СМЕНА КЛАССА!')
            pixmap = QPixmap(f"Images/Monsters/monster ({str(self.id_card)}).jpg")
            self.place_class.setPixmap(pixmap)
            if self.name[-1].isdigit():
                class_mun = self.name[:-1]
            else:
                class_mun = self.name
            self.close()
            self.close()

    def taker_for_race(self):  # взятие расс
        global race, class_mun

        if self.place_race.pixmap() is None:
            pixmap = QPixmap(f"Images/Monsters/monster ({str(self.id_card)}).jpg")
            self.place_race.setPixmap(pixmap)
            if self.name[-1].isdigit():
                race = self.name[:-1]
            else:
                race = self.name
            self.close()
        else:
            self.command_string.setText('СМЕНА РАСЫ!')
            pixmap = QPixmap(f"Images/Monsters/monster ({str(self.id_card)}).jpg")
            self.place_race.setPixmap(pixmap)
            if self.name[-1].isdigit():
                race = self.name[:-1]
            else:
                race = self.name
            self.close()

    def fight_monster(self):
        if int(self.damage) > int(self.lvl_d):
            self.close()
            self.type_c, self.idd, self.thing, self.num_treasures = 1, self.id_card, 0, self.treasure
        else:
            self.close()
            self.type_c, self.idd, self.thing, self.num_treasures = 0, 0, '-', 0

    def escaping(self):
        if self.escape is not None:
            if self.escape > 4:
                self.command_string.setText('Нажмите обновить снизу экрана')
                self.type_c, self.idd, self.thing, self.num_treasures = 2, 0, '-', 0
                self.close()
            else:
                self.command_string.setText('Нажмите обновить снизу экрана')
                self.type_c, self.idd, self.thing, self.num_treasures = 0, 0, '-', 0
                self.close()
        else:
            self.command_string.setText('Нажмите на кнопку костей и снова на карту')
            self.close()

    def fight_or_run(self):
        return self.type_c, self.idd, self.thing, self.num_treasures

    def show_card(self):
        pixmap = QPixmap(f"Images/Monsters/monster ({str(self.id_card)}).jpg")
        self.res.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = First()
    w.show()  # открываем начальное окно - приветсвия
    sys.exit(app.exec_())
