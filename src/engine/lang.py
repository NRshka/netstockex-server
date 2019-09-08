'''
Описывает классы комманд языка
@author ADT
'''
from dataclasses import dataclass


from .machine import *





class Socket:
    def __init__(self, port: int):
        self.port = port - 1

    def run(self, computer) -> int:
        if self.port < 1 or self.port > len(computer.ports):
            return -1

        if computer.ports[self.port]:
            return -2

        computer.ports[self.port] = True

        return 0


    def close(self, computer) -> int:
        '''
        Закрывает порт на компьютере
        Возвращает -1 если порт уже закрыт
        '''
        if computer.ports[self.port]:
            computer.ports[self.port] = False
            return 0

        return -1


    def sendto(self, packet: dict, ip: str, port: int, computer):
        '''
        Отправляет сообщение в соответствующий интерфейст компьютера
        Возвращает -1, если нет подходящего сетевого интерфейса
        '''
        if len(computer.interfaces) < 0:
            return -1

        packet['from_ip'] = computer.ip
        packet['from_port'] = computer.port
        packet['to_ip'] = ip
        packet['to_port'] = port
        #packet['data'] = 

        computer.interfaces.sendto(packet, ip, port)
        return 0


    def recvfrom(self, port: int, computer):# -> dict, str, int:
        '''
        Регистрирует listener-a на порту компьютера
        Блокирует поток выполнения
        @params
        port: int
        computer
        @returns
        packet: dict
        address: str, ip address of sender
        port: int, port of sender
        '''
        computer.add_listener(port)