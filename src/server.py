# import asyncio
from socket import *
#
#
from user import logining


sock = socket(AF_INET, SOCK_DGRAM)


def work(request: bytes) -> bytes:
    '''
    Обрабатывает пользовательские запросы, является event loop
    @params
    request: запрос в байтах
    @returns
    None
    '''
    data = request.split(b'\0')
    resp = b''
    if data[0] == b'log':
        username = str(data[1], 'utf-8')
        pass_hash = str(data[2], 'utf-8')

        if logining.login(username, pass_hash):
            resp = b'okey'
        else:
            resp = b'nope'

    elif data[0] == b'reg':
        username = str(data[1], 'utf-8')
        pass_hash = str(data[2], 'utf-8')
        email = str(data[3], 'utf-8')

        if logining.register(username, email, pass_hash):
            resp = b'okey'
        else:
            resp = b'nope'

    return resp


def handler() -> None:
    sock.listen()
    conn, addr = sock.accept()
    data = sock.recvfrom(512)
    resp = work(data)
    sock.sendto(resp, addr)


if __name__ == "__main__":
    sock.bind(('', 1355))
    handler()
