'''
Модуль, содержащий инструменты для генерации и работы с данными,
которые используются как исходный материал для вычислений на аукционе
@author ADT
'''
#TODO typing.Dict
import random
import string
from typing import Optional
from dataclasses import dataclass


class Packet:
    def __init__(self, ready_packet: Optional[dict]=None, data: Optional[bytes]=None,
                from_ip: Optional[str]=None, from_port: Optional[str]=None,
                dest_ip: Optional[str]=None, dest_port: Optional[str]=None):
        if ready_packet:
            self.from_ip: str = ready_packet['from_ip']
            self.from_port: str = ready_packet['from_port']
            self.to_ip: str = ready_packet['to_ip']
            self.to_port: str = ready_packet['to_port']
            self.data: bytes = ready_packet['data']
        else:
            assert data and from_port and from_ip and dest_port and dest_ip, 'Need all items'
            self.from_ip: str = from_ip
            self.to_ip: str = dest_ip
            self.from_port: str = from_port
            self.to_port: str = dest_port
            self.data: bytes = data


    def __str__(self):
        string_form = f'Source ip: {self.from_ip}\n\rSource port: {self.from_port}\n\r'
        string_form += f'Destination ip: {self.to_ip}\n\rDestination port: {self.to_port}\n\r'
        string_form += f'{self.data}'
        return string_form


    def __eq__(self, another):
        if not type(another) == type(self):
            return False

        for key in self.__dict__:
            try:
                if not (self.__dict__[key] == another.__dict__[key]):
                    return False
            except KeyError:
                return False

        return True


@dataclass
class Letter:
    title: str
    sender: str
    recipient: str
    text: str
    date: str

    def __str__(self):
        strf: str = ''
        for key in self.__dict__:
            strf += self.__dict__[key]
            strf += '\0'

        return strf


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