'''
Модуль, содержащий инструменты для генерации и работы с данными,
которые используются как исходный материал для вычислений на аукционе
@author ADT
'''
import random
import string


def random_name(minl: int = 2, maxl: int = 15) -> str:
    '''
    генерирует рандомный набор символов, похожий на имя переменной
    используется, например, для именования столбцов в csv данных
    @params
    minl: int, минимальная длина
    maxl: int, максимальная длина
    @returns
    str
    '''
    name = ''
    length = random.randint(minl, maxl+1)

    for i in range(length):
        name += random.choice(string.ascii_lowercase)

    return name


def create_csv(count_columns: int, count_rows: int) -> str:
    assert count_columns > 0
    assert count_rows > 0

    data = {}
    columns = [random_name() for i in count_columns]