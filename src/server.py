# import asyncio
import threading
import docstring
from socket import socket, AF_INET, SOCK_DGRAM
#
#
from user import logining
from engine.stock import Stock


sock = socket(AF_INET, SOCK_DGRAM)
stockex = Stock()


def work(request: bytes) -> bytes:
    '''
    Обрабатывает пользовательские запросы, является event loop
    @params
    request: запрос в байтах
    @returns
    None
    '''
    print('Request:', request)
    data = request.split(b'\0')
    resp = b''
    if data[0] == b'log':
        username = str(data[1], 'utf-8')
        pass_hash = str(data[2], 'utf-8')

        if logining.login(username, pass_hash):
            resp = b'okey'
        else:
            resp = b'nope'
        print('Log', str(resp, 'utf-8'))
    elif data[0] == b'reg':
        username = str(data[1], 'utf-8')
        pass_hash = str(data[2], 'utf-8')
        email = str(data[3], 'utf-8')

        if logining.register(username, email, pass_hash):
            resp = b'okey'
        else:
            resp = b'nope'
        print('Reg', str(resp, 'utf-8'))
    elif data[0] == b'stock':
        for task in stockex.tasks:
            resp += bytes(str(task.herz), 'utf-8')
            resp += b'\0'
            resp += bytes(str(task.paral_degree), 'utf-8')
            resp += b'\0'
            resp += bytes(str(task.storage_mem), 'utf-8')
            resp += b'\0'
            resp == bytes(task.deadline.strftime('%d-%m-%Y/%H:%M'), 'utf-8')
            resp += b'\0'

    return resp


def handler() -> None:
    #sock.listen()
    #conn, addr = sock.accept()
    data, addr = sock.recvfrom(512)
    resp = work(data)
    print(resp)
    sock.sendto(resp, addr)


def reload_stock_tasks(stop_func):
    stockex.generate_tasks()
    if not stop_func.is_set():
        threading.Timer(60, reload_stock_tasks, [stop_func]).start()


if __name__ == "__main__":
    sock.bind(('', 1355))
    a = ''
    stop_func = threading.Event()
    reload_stock_tasks(stop_func)

    while True:
        print('Waiting for input...')
        a = input()
        if a == 'q':
            break

        handler()
