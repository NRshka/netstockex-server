'''
Модуль, реализующий функционал работы ЭВМ
Скорость измеряется в байтах в секунду
Объём измеряется в мегабайтах
Частота измеряется в герцах
@author ADT
'''
import time
from typing import List, Optional, Dict, Any
from collections import namedtuple
from datetime import datetime
from overrides import overrides
from dataclasses import dataclass


current_millisecs_time = lambda: int(round(time.time() * 1000))


def compare_ip(ip_net: List[int], mask_net: List[int], dest_ip: List[int]) -> bool:
    '''
    Checks whether ip address belongs to the specified subnetwork
    @params
    ip_net: list of str, ipv4 or ipv6 address of subnetwork
    mask_net: list of str, same sort of ip_net, mask of net (orly?)
    dest_ip: ip address of destination, has same sort as previous things
    @return
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


def apply_mask(ip_net: List[int], net_mask: List[int]) -> List[int]:
    '''
    Apply mask to ip address
    @params
    ip_net: ip address of computer
    net_mask: mask of network
    @return
    ip address of network
    '''
    assert len(ip_net) == len(net_mask)
    net_addr: List[int] = [a&b for a, b in zip(ip_net, net_mask)]
    return net_addr 


def get_new_ip(net_addr: List[int], count: int) -> List[int]:
    assert count > 0 

    new_addr: List[int] = [i for i in net_addr]
    number: int = count
    ind: int = len(net_addr) - 1
    while number > 0:
        new_addr[ind] += number % 255
        if new_addr[ind] > 254:
            new_addr[ind - 1] += new_addr[ind] // 254
            new_addr[ind] = new_addr[ind] % 254

        ind -= 1
        number = number // 255

    return new_addr


#Batch = namedtuple('Batch', ['item', 'passed', 'time', 'delegate', 'args'])
@dataclass
class Batch:
    item: object
    passed: int
    time: int
    delegate: Any
    args: dict


class Pump:
    coming: list
    processing: list
    time_last_pumping: int
    def __init__(self):
        self.coming: list = []
        self.processing: list = []
        self.time_last_pumping: int = current_millisecs_time()


    def spit(self, batch):
        assert batch.time >= 0, ValueError("Can't be negative")

        if batch.time > 0:
            self.coming.append(batch)
        else:#time == 0
            self.processing.append(item)


    def spit_item(self, item, consuming_time):
        assert consuming_time >= 0, ValueError("Can't be negative")

        if consuming_time > 0:
            self.coming.append(Batch(item, 0, consuming_time))
        else:#time == 0
            self.processing.append(item)


    def pump(self):
        '''
        '''
        # I use the while loop here because
        # the container cannot be changed in the for loop
        # it can lead to IndexError.
        current_time: int = current_millisecs_time()
        delta_time: int = current_time - self.time_last_pumping
        self.time_last_pumping = current_time

        ind = 0
        while ind < len(self.coming):
            batch = self.coming[ind]
            batch.passed += delta_time
            if batch.passed >= batch.time:
                self.coming.remove(batch)
                self.processing.append(batch)
                batch.delegate(**batch.args)
            else:
                ind += 1


class NonNegativeDesc:
    '''
    Descriptor class to set non negative numeric values
    '''
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        # if the value isn't numeric it'll rise TypeError
        # because python can't do non numeric < 0
        # if it implemented into class - class must to provide numeric things
        if value < 0:
            raise ValueError("Can't be negative")

        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Machine(Pump):
    '''
    Clss of user machine to do any calculations
    '''
    hz = NonNegativeDesc()
    threads = NonNegativeDesc()
    ram_mem = NonNegativeDesc()
    storage_mem = NonNegativeDesc()
    storage_speed = NonNegativeDesc()
    net_speed = NonNegativeDesc()
    # pylint: disable=too-many-arguments
    def __init__(self, hz: int, threads: int, ram_mem: int,
                storage_mem: int, storage_speed: int, net_speed: int,
                name: Optional[str] = None):
        
        super().__init__()

        self.name = name

        self.hz = hz
        self.threads = threads
        self.ram_mem = ram_mem
        self.storage_speed = storage_speed
        self.storage_mem = storage_mem
        self.net_speed = net_speed

        self.gateway = None
        self.ip_addr = None
        self.net_mask = None
        self.ports = [None for _ in range(2**16)]

        self.queue: List[list] = []


    def set_net_data(self, ip_addr: List[int], net_mask: List[int], gateway, ipv6=None):
        '''

        '''
        assert ipv6 is None, "ipv6 hasn't done"
        #TODO: check length == 4 and 0 < byte < 255

        self.ip_addr = ip_addr
        self.net_mask = net_mask
        ones = [255 for _ in range(len(ip_addr))]
        last_addr = [a^b for a, b in zip(ones, net_mask)]
        self.broadcast: List[int] = [a|b for a, b in zip(ip_addr, last_addr)]
        self.gateway = gateway


    def set_gateway(self, gateway):
        self.gateway = gateway


    def take_packet(self, packet: dict, test_dict: Optional[dict]=None):
        '''
        If destination ip is there, send packet to
        a socket associated with the port of destination
        @params
        packet: dict with headers
        @return
        None
        '''

        port = packet['to_port']
        print(self.name, ':')
        print(packet)
        test_dict['packet'] = packet
        test_dict['recipient'] = self
        #if self.ports[]


    def send_packet(self, packet: dict, test_dict: Optional[dict]=None):
        '''
        Low-level method shouldn't be used by users
        Should Add command "send packet" to pumping
        '''
        send_command = Batch(packet, 0, 10000, self.gateway.take_packet, dict(
            packet=packet, test_dict=test_dict
        ))
        self.spit(send_command)
        #self.gateway.take_packet(packet, test_dict)


    def add_program(self, data, program: list) -> int:
        '''
        Add soft to queue of runing programs
        @params
        data: data to ru program
        program: list of commands
        @return seconds
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
        @return
        count of existing entries as result of this function
        '''

        self.ip_table.append(self.IP_row(ip_net, ip_mask, interface))

        return len(self.ip_table)


    def connect_machine(self, interface: str, device: Machine):
        #TODO отключить машину по ту сторону провода от этой
        self.interfaces_table[interface] = device


    @overrides
    def take_packet(self, packet: dict, test_dict: Optional[dict]=None):
        '''
        Find packet and find most suitable interface to send forward
        @params
        packet: dict, iternet packet with headers
        @return
        None
        '''
        str_f_ip: List[str] = packet['to_ip'].split('.')
        dest_ip: List[int] = [int(i) for i in str_f_ip]
        del str_f_ip

        for row in self.ip_table:
            if compare_ip(row.ip_net, row.ip_mask, dest_ip):
                try:
                    next_mach = self.interfaces_table[row.interface]
                    next_mach.take_packet(packet, test_dict)
                except KeyError:
                    time_now: str = datetime.now().strftime("%d-%m-%Y/%H:%M")
                    self.log.append(f'[{time_now}] No connected device at {row.interface} \
                                    interface')
                finally:
                    return
        #if there are no suitable devices:
        dg: str = self.default_gateway
        try:
            self.interfaces_table[dg].take_packet(packet, test_dict)
        except KeyError:
            time_now: str = datetime.now().strftime("%d-%m-%Y/%H:%M")
            self.log.append(f'[{time_now}] No connected device at {dg} interface')


class Switcher(Machine):
    '''
    Switcher to route packets in subnetwork
    '''
    #pylint disable=too-many-instance-attributes
    def __init__(self, net_addr: List[int], net_mask: List[int], name: Optional[str]=None):
        super().__init__(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3, name=name)
        self.switch_table = {}#'192.168.1.92': 'eth1' form
        self.interfaces_table = {}#matchnig interface name string and Machine class
        self.log: List[str] = []#errors
        self.net_addr: List[int] = net_addr
        self.net_mask: List[int] = net_mask
        self.count_devices = 0#count of connected devices
        
        self.max_devices = -2#cause first address is the address of network, last is broadcast
        for ind, item in enumerate(reversed(self.net_mask)):
            self.max_devices += (item^255)*(255**(ind+1))
        assert self.max_devices >= 0, 'incorrect net mask'


    @overrides
    def set_gateway(self, gateway):
        self.gateway = gateway


    @overrides
    def take_packet(self, packet: dict, test_dict: Optional[dict] = None):
        try:
            ip_addr: str = packet['to_ip']
            interface: str = self.switch_table[ip_addr]
            device = self.interfaces_table[interface]
            device.take_packet(packet, test_dict)
        except KeyError:
            #send to default gateway
            self.gateway.take_packet(packet, test_dict)
            #time_now: str = datetime.now().strftime("%d-%m-%Y/%H:%M")
            #self.log.append(f'[{time_now}] No connected device or wrong packet')


    def connect_machine(self, interface: str, device: Machine, ip: Optional[str] = None) -> int:
        '''
        Если задан ip, не меняет насроет подключаемой машины,
        предполагаеся, что раз уж задаёте - сами настроили
        Иначе настраиваее машину, выдавая ip and net mask
        Returns status code
        '''
        #TODO отключить машину по ту сторону провода от этой
        if self.count_devices > self.max_devices:
            return -1
        self.interfaces_table[interface] = device
        if ip is None:
            new_ip: List[int] = get_new_ip(self.net_addr, self.count_devices + 1)
            strfip: str = '.'.join([str(i) for i in new_ip])
            self.switch_table[strfip] = interface
            device.set_net_data(new_ip, self.net_mask, self)
        else:
            self.switch_table[ip] = interface
        self.count_devices += 1


class PostServer(Machine):
    '''
    '''
    def __init__(self):
        super().__init__(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3)
        self.Letter = namedtuple('Letter', 'status title sender recipient text date')
        self.mail = {}#recipient address: [Letter]
        self.post_ips: Dict[str, str] = {}#ip address of other mail server
        self.dns_ip = {}#addresses of dns servers


    @overrides
    def take_packet(self, packet: dict, test_dict: Optional[dict]=None):
        '''
        Take packet in form of post mail
        If protocol not corfimed log it
        '''
        #if it isn't recipient drop packet
        port: int = int(packet['to_port'])
        if packet['to_ip'] != self.ip_addr or self.ports[port] is None:
            return

        try:
            things: List[bytes] = packet['data'].split(b'\0')
            title: str = str(things[0], 'utf-8')
            sender: str = str(things[1], 'utf-8')
            recipient: str = str(things[2], 'utf-8')
            text: str = str(things[3], 'utf-8')
            date: str = str(things[4], 'utf-8')
        except (IndexError, KeyError):
            #error in protocol, drop
            return
        
        new_letter = self.Letter('new', title, sender, recipient, text, date)
        self.mail[recipient].append(new_letter)


    def send_mail(self, letter: dict) -> int:
        recip_server_name: str = ''
        try:
            recip_server_name = letter['recipient'].split('@')[1]
        except KeyError:
            return -1

        try:
            ip_addr = self.post_ips[recip_server_name]
            letter['from'] = '.'.join(self.ip_addr)
            letter['to'] = ip_addr
            data = b'\0'.join([bytes(letter[field], 'utf-8') for field in letter])
            self.gateway.take_packet(data)
        except:
            #send requese to dns server to find ip address of post server
            pass



class DNSResolver(Machine):
    '''
    Adds an address entry to the ip address, creates an entry if it did not exist.
    '''
    def __init__(self):
        super().__init__(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3)
        self.table = {}
        self.table[b'mx'] = {}


    def add_entry(self, req:bytes, names:List[bytes], ip_list: List[bytes]):
        '''
        '''
        try:
            self.table[req]
        except KeyError:
            self.table[req] = {}

        for name in names:
            try:
                for ip_addr in ip_list:
                    self.table[req][name].append(ip_addr)
            except KeyError:
                self.table[req][name] = []
                for ip_addr in ip_list:
                    self.table[req][name].append(ip_addr)


    @overrides
    def take_packet(self, packet: dict, test_dict: Optional[dict] = None):
        req: bytes = b''
        address: bytes = b''
        key: bytes = b''
        try:
            things: List[bytes] = packet['data'].split(b'\0')
            req = things[0]
            address = things[1]
            key = things[2]
        except (IndexError, KeyError):
            return

        try:
            resp: bytes = self.table[req][address][0]
            data: bytes = b'\0'.join([resp, key])
            #answer = {k: packet[k] for k in packet if k != 'data'}
            answer = {
                'from_ip': packet['to_ip'],
                'to_ip': packet['from_ip']
            }
            answer['data'] = data
            #TODO process the case whe gateway isn't set
            self.gateway.take_packet(answer)
        except KeyError:
            #this dns server doesn't know
            pass
