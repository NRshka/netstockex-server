import objgraph
from datetime import datetime
from random import choice
from string import ascii_letters


from engine import *


def generate_text(length: int) -> str:
    s = ''
    for i in range(length):
        s += choice(ascii_letters + ' ')
    return s


def generate_dns_request(type_req: str, addr: str, resolver: str, from_ip: str) -> bytes:
    packet: dict = {}
    packet['from_ip'] = from_ip
    packet['to_ip'] = resolver

    data: bytes = b''
    data += bytes(type_req, 'utf-8') + b'\0'
    data += bytes(addr, 'utf-8') + b'\0'
    key: str = generate_text(16)
    data += bytes(key, 'utf-8')

    packet['data'] = data

    return packet


if __name__ == "__main__":
    count_endpoints = 3
    mask = [255, 255, 255, 0]

    m1 = Machine(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name='Machine1')
    m2 = Machine(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name='Machine2')
    m3 = Machine(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name='Machine3')
    m4 = Machine(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name='Machine4')

    r1 = Router('eth0', name='Router1')
    r2 = Router('eth0', name='Router2')

    s1 = Switcher(net_addr=[192, 168, 44, 0], net_mask=mask, name='Switcher1')
    s1.set_gateway(r1)
    s2 = Switcher(net_addr=[12, 16, 87, 0], net_mask=mask, name='Switcher2')
    s2.set_gateway(r2)
    s3 = Switcher(net_addr=[64, 27, 55, 0], net_mask=mask, name='Switcher3')

    d1 = DNSResolver()
    d1.add_entry(b'mx', [b'mailmaster'], [b'12.16.87.15'])
    d1.set_gateway(s1)

    p1 = PostServer()
    #p1.set_gateway()

    m1ip = [192, 168, 44, 82]
    m2ip = [12, 16, 87, 16]
    m3ip = [192, 168, 44, 83]
    m1.set_net_data(m1ip, mask, s1)
    m2.set_net_data(m2ip, mask, s2)
    m3.set_net_data(m3ip, mask, s1)
    m1.set_gateway(s1)
    m2.set_gateway(s2)
    m3.set_gateway(s1)

    s1.connect_machine('eth1', m1, '.'.join([str(i) for i in m1ip]))
    s1.connect_machine('eth2', m3, '.'.join([str(i) for i in m3ip]))
    s1.connect_machine('eth3', d1, '192.168.44.81')
    s1.connect_machine('eth0', r1)

    r1.connect_machine('eth0', r2)
    r1.connect_machine('eth1', s1)

    r2.connect_machine('eth0', r1)
    r2.connect_machine('eth1', s2)

    s2.connect_machine('eth0', r2)
    s2.connect_machine('eth1', m2, '.'.join([str(i) for i in m2ip]))

    r1.add_trace(m2ip, mask, 'eth0')
    r1.add_trace(m1ip, mask, 'eth1')
    r2.add_trace(m1ip, mask, 'eth0')
    r2.add_trace(m2ip, mask, 'eth1')


    dns_req: bytes = generate_dns_request('mx', 'mailmaster', '192.168.44.81', '.'.join([str(i) for i in m1ip]))
    #m1.send_packet(dns_req)
    #p1 = Packet(data=b'First packet', from_ip='.'.join([str(i) for i in m1ip]), from_port='6886',
    #            dest_ip='.'.join([str(i) for i in m2ip]), dest_port='1337')
    #p2 = Packet(data=b'Second packet', from_ip='.'.join([str(i) for i in m2ip]), from_port='1337',
    #            dest_ip='.'.join([str(i) for i in m1ip]), dest_port='6886')
    #p3 = Packet(data=b'Third packet')
    ip_ads = [m1ip, m2ip, m3ip]
    machines = [m1, m2, m3]
    packets = []
    all_devices = [m1, m2, m3, m4, r1, r2, s1, s2]
    for i in range(count_endpoints):
        for j in range(count_endpoints):
            if i == j:
                continue

            test_dict = {}
            packet = Packet(
                data=bytes(str(i+1)+' to '+str(j+1), 'utf-8'),
                from_ip='.'.join([str(ip) for ip in ip_ads[i]]),
                from_port='6468',
                dest_ip='.'.join([str(ip) for ip in ip_ads[j]]),
                dest_port='1111'
            )
            machines[i].send_packet(packet.__dict__, test_dict)

            IS_NEED_PUMP = True
            while IS_NEED_PUMP:
                IS_NEED_PUMP = False
                for device in all_devices:
                    if len(device.coming) > 0:
                        IS_NEED_PUMP = True
                        device.pump()

            assert test_dict['packet'] == packet.__dict__
            assert test_dict['recipient'] == machines[j]


    l1 = Letter(
        title='First email',
        sender='machine1@mailmaster.com',
        recipient='machine2@mailmaster.com',
        text='c374hfvc39pbvnc 7hv475v4bv vh549g7h3pabv 3fg37b30v 3v3p4bgf3gv 3vb54804v 459!',
        date=datetime.now().strftime("%d-%m-%Y/%H:%M")
    )
    l1bytes = bytes(str(l1), 'utf-8')

    l2 = Letter(
        title='First email',
        sender='machine1@mailmaster.com',
        recipient='machine2@mailmaster.com',
        text='c374hfvc39pbvnc 7hv475v4bv vh549g7h3pabv 3fg37b30v 3v3p4bgf3gv 3vb54804v 459!',
        date=datetime.now().strftime("%d-%m-%Y/%H:%M")
    )
    l2bytes = bytes(str(l2), 'utf-8')

    roots = objgraph.get_leaking_objects()
    print(len(roots))
    objgraph.show_most_common_types(objects=roots)
