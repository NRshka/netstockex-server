from engine import *



if __name__ == "__main__":
    m1 = Machine(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name='Machine1')
    m2 = Machine(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name='Machine2')
    r1 = Router('eth0')
    r2 = Router('eth0')

    m1ip = [192, 168, 44, 82]
    m2ip = [12, 16, 87, 16]
    m1.set_net_data(m1ip, [255, 255, 255, 0], r1)
    m2.set_net_data(m2ip, [255, 255, 255, 0], r2)
    m1.set_gateway(r1)
    m2.set_gateway(r2)

    r1.connect_machine('eth0', r2)
    r2.connect_machine('eth0', r1)
    r1.connect_machine('eth1', m1)
    r2.connect_machine('eth1', m2)
    r1.add_trace(m2ip, [255, 255, 255, 0], 'eth0')
    r1.add_trace(m1ip, [255, 255, 255, 0], 'eth1')
    r2.add_trace(m1ip, [255, 255, 255, 0], 'eth0')
    r2.add_trace(m2ip, [255, 255, 255, 0], 'eth1')

    p1 = Packet(data=b'First packet', from_ip='.'.join([str(i) for i in m1ip]), from_port='6886',
                dest_ip='.'.join([str(i) for i in m2ip]), dest_port='1337')
    p2 = Packet(data=b'Second packet', from_ip='.'.join([str(i) for i in m2ip]), from_port='1337',
                dest_ip='.'.join([str(i) for i in m1ip]), dest_port='6886')

    m1.send_packet(p1.__dict__)
    m2.send_packet(p2.__dict__)
