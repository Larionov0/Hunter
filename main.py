from msvcrt import getch
from os import system
import random
from time import sleep


def press():
    return getch().decode()


def press2():
    a = input()
    return a


def clear():
    system('cls')


def distance(coords1, coords2):
    a = coords2[0] - coords1[0]
    b = coords2[1] - coords1[1]
    c = (a*a + b*b) ** 0.5
    return c


def create_matrix(n, m):
    matrix = []
    i = 0
    while i < n:
        row = ['-'] * m
        matrix.append(row)
        i += 1
    return matrix


def print_matrix(matrix):
    for row in matrix:
        text = "|"
        for kletka in row:
            text += kletka + " "
        text = text[:-1] + "|"
        print(text)


def creature_to_pole(pole, creature):
    coords = creature["coords"]
    pole[coords[0]][coords[1]] = creature["face"]


def player_make_hod(pole, hero, animals, store):
    store_access = hero['coords'] == [len(pole) - 1, len(pole[0]) - 1]

    coords = hero["coords"]
    pole[coords[0]][coords[1]] = '-'
    print('--= Main menu =--')
    print('Детали: ' + str(hero['details']))
    print('Стрелы: ' + str(hero['arrows']))
    print('Камни: ' + str(hero['rocks']))

    if hero['weapon'] is not None:
        print(f'Ваше оружие: {hero["weapon"]["type"]}  (Урон: {hero["weapon"]["damage"]}  Дальность: {hero["weapon"]["range"]})')
    else:
        print("Вы с голыми руками. Ловите куриц!")
    print("WASD")
    if hero['weapon'] is not None:
        print("x - выстрел")

    if store_access:
        print('z - магазин')

    print("e - inventory")

    choice = press()

    if choice in ['w', 'a', 's', 'd']:
        hero_move(choice, coords)
    elif choice == "x" and hero['weapon'] is not None:
        hero_piw(hero, pole, animals)
    elif choice == 'z' and store_access:
        store_menu(hero, store)
    elif choice == 'e':
        inventory_menu(hero)


def inventory_menu(hero):
    while True:
        clear()
        print("---= Ваш инвентарь =---")
        print('0 - выход из инфвентаря')
        print('1 - мое оружие')

        choice = input("Ваш выбор: ")
        if choice == '0':
            return
        elif choice == '1':
            print("0 - назад")
            i = 1
            for weapon in hero['inventory']['weapons']:
                print(f'{i} - {weapon["type"]} {weapon["name"]}  (Урон: {weapon["damage"]}  Дальность: {weapon["range"]})')
                i += 1

            number = int(input("Ваш выбор: "))
            if number == 0:
                continue
            if number < 0 or number > len(hero['inventory']['weapons']):
                print("Не существует")
                input("<Enter>")

            weapon = hero['inventory']['weapons'][number - 1]

            print(f"Вы выбрали: {weapon['name']}. Что сделать?")

            print('1 - выбросить')
            print('2 - назначить как главное')
            print('3 - разобрать на детали')
            choice = input("Выберите номер: ")

            if choice == '1':
                hero['inventory']['weapons'].remove(weapon)
                if hero['weapon'] is weapon:
                    hero['weapon'] = None
            elif choice == '2':
                hero['weapon'] = weapon
            elif choice == '3':
                pass


def store_menu(hero, store):
    while True:
        clear()
        print('--= Store =--')
        print('Детали: ' + str(hero['details']))
        print('Стрелы: ' + str(hero['arrows']))
        print('Камни: ' + str(hero['rocks']))
        print(f"Инвентарь: {hero['inventory']}")

        if hero['weapon'] is not None:
            print(
                f'Ваше оружие: {hero["weapon"]["type"]}  (Урон: {hero["weapon"]["damage"]}  Дальность: {hero["weapon"]["range"]})')
        else:
            print("Вы с голыми руками. Ловите куриц!")

        print("Выберите секцию: ")
        i = 1
        print('0 - выход из магазина')
        for section_name in store:
            print(f"{i} - {section_name}")
            i += 1

        choice = int(input("Выберите секцию: "))
        if choice == 0:
            return

        if 0 > choice or choice > len(store):
            print("Некорректный выбор!")
            continue

        section_name = list(store.keys())[choice - 1]

        if section_name == 'weapons':
            print("0 - назад в магазин")
            i = 1
            for weapon in store['weapons']:
                print(f"{i} - {weapon['details']} деталей - {weapon['type']} {weapon['name']}  ({weapon['damage']} урона, {weapon['range']} клеток)")
                i += 1
            number = int(input("Выберите номер: "))

            if number == 0:
                continue

            if number > len(store['weapons']):
                print("Недоступно!")
                continue

            weapon = store['weapons'][number - 1]
            if hero['details'] >= weapon['details']:
                print("Приобретено!")
                hero['details'] -= weapon['details']
                hero['inventory']['weapons'].append(weapon.copy())
                input("<Enter>")
                continue
            else:
                print("Недостаточно деталей!!")
                input("<Enter>")


        elif section_name == 'ammo':
            print("0 - назад в магазин")
            i = 1
            for ammo in store['ammo']:
                print(f"{i} - {ammo['details']} деталей - {ammo['type']}   ({ammo['count']} количество)")
                i += 1
            number = int(input("Выберите номер: "))
            if number == 0:
                continue
            if number > len(store['ammo']):
                print("Недоступно!")
                continue
            ammo = store['ammo'][number - 1]
            if hero['details'] >= ammo['details']:
                print("Приобретено!")
                hero['details'] -= ammo['details']
                if ammo["type"] == "arrow":
                    hero['arrows'] += ammo["count"]
                elif ammo["type"] == "rocks":
                    hero['rocks'] += ammo["count"]
                input("<Enter>")
                continue
            else:
                print("Недостаточно деталей!!")
                input("<Enter>")


def hero_move(choice, coords):
    if choice == "w":
        if coords[0] != 0:
            coords[0] -= 1
    elif choice == "a":
        if coords[1] == 0:
            coords[1] = m - 1
        else:
            coords[1] -= 1
    elif choice == "s":
        if coords[0] != n - 1:
            coords[0] += 1
    elif choice == "d":
        if coords[1] == m - 1:
            coords[1] = 0
        else:
            coords[1] += 1


def hero_piw(hero, pole, animals):
    if hero['weapon']['type'] == 'bow':
        if hero['arrows'] > 0:
            print("Выбери направление (WASD)")
            choice = press()

            arrow = {
                'damage': hero['weapon']['damage'],
                'coords': hero['coords'].copy(),
                'energy': hero['weapon']['range'],
                'direction': choice,
                'face': 'x'
            }
            hero['arrows'] -= 1
            arrow_flying(arrow, pole, animals, hero)
        else:
            input("Нехватает стрел!")

    elif hero['weapon']['type'] == 'slingshot':
        if hero['rocks'] > 0:
            i = 0
            while i < len(pole):
                j = 0
                while j < len(pole[i]):
                    coords = [i, j]
                    if distance(coords, hero['coords']) <= hero['weapon']['range']:
                        if pole[i][j] == '-':
                            pole[i][j] = '+'
                        if pole[i][j] == 'k':
                            pole[i][j] = 'K'
                    j += 1
                i += 1
            clear()
            print_matrix(pole)

            animals_near_hero = find_all_animals_near_hero(hero, animals, hero['weapon']['range'])
            if len(animals_near_hero) == 0:
                input("Нету живности рядом :(")
                delete_decorations(pole)
                return

            i = 0
            for animal in animals_near_hero:
                print(str(i) + ' - ' + animal['name'] + ' (' + str(animal['hp']) + ' hp)')
                i += 1
            choice = int(input('Выберите животное: '))

            target_animal = animals_near_hero[choice]
            damage_to_animal(target_animal, hero['weapon']['damage'], animals, pole)
            delete_decorations(pole)
            hero['rocks'] -= 1


def delete_decorations(pole):
    decorations = ['+', '?']

    for row in pole:
        j = 0
        while j < len(row):
            if row[j] in decorations:
                row[j] = '-'
            j += 1


def find_all_animals_near_hero(hero, animals, d):
    animals_near_hero = []
    for animal in animals:
        if distance(animal['coords'], hero['coords']) <= d:
            animals_near_hero.append(animal)
    return animals_near_hero


def arrow_flying(arrow, pole, animals, hero):
    direction = arrow['direction']

    while arrow['energy'] > 0:
        clear()
        print_matrix(pole)
        sleep(0.05)
        pole[arrow['coords'][0]][arrow['coords'][1]] = '-'
        if direction == 'w':
            arrow['coords'][0] -= 1
        elif direction == 'a':
            arrow['coords'][1] -= 1
        elif direction == 's':
            arrow['coords'][0] += 1
        elif direction == 'd':
            arrow['coords'][1] += 1

        pole[arrow['coords'][0]][arrow['coords'][1]] = arrow['face']
        pole[hero['coords'][0]][hero['coords'][1]] = hero['face']

        for animal in animals:
            if arrow['coords'] == animal['coords']:
                damage_to_animal(animal, arrow['damage'], animals, pole)
                pole[arrow['coords'][0]][arrow['coords'][1]] = '-'
                return

        arrow['energy'] -= 1
    pole[arrow['coords'][0]][arrow['coords'][1]] = '-'


def damage_to_animal(animal, damage, animals, pole):
    animal['hp'] -= damage
    if animal['hp'] <= 0:
        animals.remove(animal)
        give_reward_to_hero(hero, animal['type'])
        pole[animal['coords'][0]][animal['coords'][1]] = '-'


def give_reward_to_hero(hero, type_):
    rewards = {
        'kurka': 3,
        'rabbit': 4,
        'zaiak': 5,
        'beef': 15,
        'pig': 8
    }

    reward = rewards[type_]
    hero['details'] += reward


def kurka_make_hod(pole, kurka):
    coords = kurka["coords"]
    pole[coords[0]][coords[1]] = '-'
    choice = random.choice(["w", "a", "s", "d"])
    if choice == "w":
        if coords[0] != 0:
            coords[0] -= 1
    elif choice == "a":
        if coords[1] == 0:
            coords[1] = m - 1
        else:
            coords[1] -= 1
    elif choice == "s":
        if coords[0] != n - 1:
            coords[0] += 1
    elif choice == "d":
        if coords[1] == m - 1:
            coords[1] = 0
        else:
            coords[1] += 1


def animals_make_hod(pole, animals):
    for animal in animals:
        if animal["type"] == "kurka":
            kurka_make_hod(pole, animal)


def animals_to_pole(pole, animals):
    for animal in animals:
        creature_to_pole(pole, animal)


def poimal_li_kurku(hero, animals):
    i = 0
    while i < len(animals):
        animal = animals[i]
        if animal["type"] == "kurka":
            if animal["coords"] == hero["coords"]:
                animals.pop(i)
                i -= 1
                hero["details"] += 3
        i += 1


def spawn_kurka(n, m, animals):
    kurka = {
        "type": "kurka",
        "name": "New",
        "face": "k",
        "hp": 3,
        "max_hp": 3,
        "coords": [random.randint(0, n - 1), random.randint(0, m - 1)]
    }
    animals.append(kurka)


n = 12
m = 18
pole = create_matrix(n, m)

hero = {
    "name": "Steeve",
    "face": "$",
    "hp": 10,
    "max_hp": 10,
    "coords": [3, 4],
    "details": 0,
    "weapon": None,
    'arrows': 10,
    'rocks': 10,
    'inventory': {
        'weapons': [],
    }
}

weapons = [
    {
        'type': 'bow',
        'damage': 4,
        'range': 4
    },
    {
        'name': 'Roga4',
        'type': 'slingshot',
        'damage': 2,
        'range': 4
    }
]

animals = [
    {
        "type": "kurka",
        "name": "Riaba",
        "face": "k",
        "hp": 3,
        "max_hp": 3,
        "coords": [1, 1]
    },
    {
        "type": "kurka",
        "name": "Masha",
        "face": "k",
        "hp": 3,
        "max_hp": 3,
        "coords": [2, 1]
    }
]


store = {
    'weapons': [
        {
            'details': 10,
            'type': 'bow',
            'name': 'base bow',
            'damage': 3,
            'range': 3
        },
        {
            'details': 30,
            'type': 'bow',
            'name': 'Bow4ik',
            'damage': 4,
            'range': 4
        },
        {
            'details': 15,
            'name': 'Roga4',
            'type': 'slingshot',
            'damage': 2,
            'range': 4
        }
    ],
    'ammo': [
        {
            'details': 5,
            'type': 'arrow',
            'count': 10
        },
        {
            'details': 25,
            'type': 'arrow',
            'count': 80
        },
        {
            'details': 4,
            'type': 'rocks',
            'count': 12
        }
    ],
    'traps': [
        {
            'details': 5,
            'type': 'mantrap',
            'damage': 10
        }
    ],
    'eat': []
}

counter = 25
while True:
    animals_to_pole(pole, animals)
    creature_to_pole(pole, hero)
    clear()
    print_matrix(pole)
    player_make_hod(pole, hero, animals, store)
    poimal_li_kurku(hero, animals)
    animals_make_hod(pole, animals)
    poimal_li_kurku(hero, animals)
    counter -= 1
    if counter == 0:
        spawn_kurka(n, m, animals)
        counter = 25

