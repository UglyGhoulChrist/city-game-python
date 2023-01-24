"""
Игра в города России, пользователь против компьютера.
*** Ход пользователя:
Пользователь начинает игру, называя первый город.
Если города нет в списке, то говорим ему, что надо назвать другой город.
Если названный город существует, заносим его в список названных городов.
Получаем первую букву с которой должен начинаеться следущий ход.
*** Ход компьютера:
Выбираем случайным образом город из списка городов,
заносим его в список названных городов.
Получаем первую букву с которой должен начинаеться следущий ход.
Передаём ход пользователю.
*** Ход игры:
Ходы игроков выводятся на экран.
Если городов не осталось, то пользователь выиграл.
"""
from itertools import cycle

check_list = []


# Функция приводит имя города в общий вид
# Будем пользоваться при получении названия города от пользователя и при загрузке списка городов из файла.
def normalize_city_name(name):
    return name.strip().lower().replace('ё', 'е')


def check_point(fun):
    check_list.append(fun)
    return fun


@check_point
def is_city_startswith_char(city, char, **kwargs):
    if char is None or city.startswith(char):
        return True
    else:
        print(f'Город должен начинаться с буквы {char.capitalize()}.')
        return False


@check_point
def is_non_cached(city, cache, **kwargs):
    if city not in cache:
        return True
    else:
        print("Этот город уже был назван.")
        return False


@check_point
def is_available(city, cities, **kwargs):
    if city in cities:
        return True
    else:
        print("Я такого города не знаю.")
        return False


def move_to_cache(city, cities, cache):
    # убираем из списка доступных
    cities.remove(city)
    # перекидываем город в кэш
    cache.add(city)


def get_next_char(city):
    wrong_char = ("Ъ", "ь", "ы", "й")
    # выбираем букву для следующего города
    for char in city[::-1]:
        if char in wrong_char:
            continue
        else:
            break
    else:
        raise RuntimeError
    return char


def user_point(char):
    user_say = input(f"{user_name}, назови город на [{char or 'любую букву'}] :")
    city = normalize_city_name(user_say)
    kw = {"char": char, "cache": cache, "cities": cities}
    if not all(x(city, **kw) for x in check_list):
        return user_point(char)
    return city


def ai_point(char):
    # выбираем город
    for city in cities:
        if city.startswith(char):
            break
    else:
        raise SystemExit(f"{user_name}, ты победил(-а)!")

    print(f"Мой ход: {str(city).capitalize()}")
    return city


def main():
    char = None
    for point in cycle((user_point, ai_point)):
        next_city = point(char)
        move_to_cache(next_city, cities, cache)
        char = get_next_char(next_city)


if __name__ == '__main__':
    print("Привет! Это игра в города России для двоих: человек и компьютер.\n")
    print("Правила игры: Первый участник называет любой город.\n"
          "Далее поочерёдно называем существующий город,\n"
          "название которого начинается на ту букву, которой оканчивается название предыдущего города.\n"
          "Исключения составляют названия, оканчивающиеся на «Ъ», «Ь», «Ы» и «Й»:\n"
          "в таких случаях участник называет город на предпоследнюю букву.\n"
          "При этом ранее названные города употреблять нельзя. \n"
          "Таймера нет, регистр ввода букв не важен.\n")
    user_name = None
    while user_name is None:
        user_name = input("Как тебя зовут? ")

    cache = set()
    with open("cities.txt", "r") as f:
        cities = {normalize_city_name(x) for x in f.readlines() if x.strip()}

    main()
