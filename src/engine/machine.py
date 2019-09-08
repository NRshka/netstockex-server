'''
Модуль, реализующий функционал работы ЭВМ
Скорость измеряется в байтах в секунду
Объём измеряется в мегабайтах
Частота измеряется в герцах
@author ADT
'''
from typing import List, Optional
from collections import namedtuple
from datetime import datetime
from overrides import overrides


def compare_ip(ip_net: List[int], mask_net: List[int], dest_ip: List[int]) -> bool:
    '''
    Checks whether ip address belongs to the specified subnetwork
    @params
    ip_net: list of str, ipv4 or ipv6 address of subnetwork
    mask_net: list of str, same sort of ip_net, mask of net (orly?)
    dest_ip: ip address of destination, has same sort as previous things
    @returns
    True if ip address refers to subnetwork else False
    '''
    if len(ip_net) != len(mask_net):
        return False
    if len(mask_net) != len(dest_ip):
        return False

    for ip_part, mask_part, dest_part in zip(ip_net, mask_net, dest_ip):
        if dest_part & mask_part != ip_part & mask_part:
            return False

    return True


class Machine:
    '''
    Clss of user machine to do any calculations
    '''
    # pylint: disable=too-many-instance-attributes
    def __init__(self, hz: int, threads: int, ram_mem: int,
                storage_mem: int, storage_speed: int, net_speed: int,
                name: Optional[str] = None):
        
        self.name = name

        assert hz > 0
        assert threads > 0
        assert ram_mem > 0
        assert storage_mem > 0
        assert storage_speed > 0
        assert net_speed > 0

        self.hz = hz
        self.threads = threads
        self.ram_mem = ram_mem
        self.storage_speed = storage_speed
        self.storage_mem = storage_mem
        self.net_speed = net_speed

        self.ports = [None for _ in range(2**16)]

        self.queue: List[list] = []


    def set_net_data(self, ip_addr: List[str], net_mask: List[int], gateway, ipv6=None):
        '''

        '''
        assert ipv6 is None, "ipv6 hasn't done"
        #TODO: check length == 4 and 0 < byte < 255

        self.ip_addr = ip_addr
        self.net_mask = net_mask
        ones = [255 for _ in range(len(ip_addr))]
        last_addr = [a^b for a, b in zip(ones, net_mask)]
        self.broadcast: List[int] = [a|b for a, b in zip(ip_addr, last_addr)]


    def set_gateway(self, gateway):
        self.gateway = gateway


    def take_packet(self, packet: dict):
        '''
        If destination ip is there, send packet to
        a socket associated with the port of destination
        @params
        packet: dict with headers
        @returns
        None
        '''

        port = packet['to_port']
        print(self.name, ':')
        print(packet)
        #if self.ports[]


    def send_packet(self, packet: dict):
        '''
        Low-level method shouldn't be used by users
        '''
        self.gateway.take_packet(packet)


    def add_program(self, data, program: list) -> int:
        '''
        Add soft to queue of runing programs
        @params
        data: data to ru program
        program: list of commands
        @returns seconds
        '''
        for command in program:
            pass


class Router(Machine):
    def __init__(self, default_gateway: str):
        super().__init__(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3)
        self.IP_row = namedtuple('IP_row', 'ip_net ip_mask interface')
        self.ip_table = []
        self.interfaces_table = {}#matching table of name of interface and Router class
        self.log = []#log of errors
        self.default_gateway = default_gateway

    def add_trace(self, ip_net: List[int], ip_mask: List[int], interface: str) -> int:
        '''
        Add a way how to collate ip address of destination and net interface
        @params
        ip_net: ip net of subnetwork
        ip_mask: ipv4/ipv6 address like [12, 10, 64, 14]
        interface: str, means gate where to kick packet to get destination
        @returns
        count of existing entries as result of this function
        '''

        self.ip_table.append(self.IP_row(ip_net, ip_mask, interface))

        return len(self.ip_table)


    def connect_machine(self, interface: str, device: Machine):
        #TODO отключить машину по ту сторону провода от этой
        self.interfaces_table[interface] = device


    @overrides
    def take_packet(self, packet: dict):
        '''
        Find packet and find most suitable interface to send forward
        @params
        packet: dict, iternet packet with headers
        @returns
        None
        '''
        str_f_ip: List[str] = packet['to_ip'].split('.')
        dest_ip: List[int] = [int(i) for i in str_f_ip]
        del str_f_ip

        for row in self.ip_table:
            if compare_ip(row.ip_net, row.ip_mask, dest_ip):
                try:
                    next_mach = self.interfaces_table[row.interface]
                    next_mach.take_packet(packet)
                except KeyError:
                    time_now: str = datetime.now().strftime("%d-%m-%Y/%H:%M")
                    self.log.append(f'[{time_now}] No connected device at {row.interface} \
                                    interface')
                finally:
                    return
        #if there are no suitable devices:
        dg: str = self.default_gateway
        try:
            self.interfaces_table[dg].take_packet(packet)
        except KeyError:
            time_now: str = datetime.now().strftime("%d-%m-%Y/%H:%M")
            self.log.append(f'[{time_now}] No connected device at {dg} interface')
