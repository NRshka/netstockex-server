'''
Модуль, реализующий функционал работы ЭВМ
Скорость измеряется в байтах в секунду
Объём измеряется в мегабайтах
Частота измеряется в герцах
@author ADT
'''
from typing import List
from collecttions import namedtuple


class Machine:
   '''

   '''
   def __init__(self, hz: int, threads: int, ram_mem: int,
               storage_mem: int, storage_speed: int, net_speed: int):
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

      self.ports = [False for _ in range(2**16)]

      self.queue: List[list] = []


      def add_program(data, program: list) -> int:
         '''
         Add soft to queue of runing programs
         @params
         data: 
         program: list of commands
         @returns seconds
         '''
         for command in program:
            pass


class Router(Machine):
   def __init__(self, default_gateway: str):
      super().__init__(21*1e5, 1, 1024, 10240, 8*1024*100, 80*1024**3)
      self.ip_table = []
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

      
      self.ip_table.append((ip_net, ip_mask, interface))

      return len(self.ip_table)

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
      if len(mask1) != len(mask2):
         return False

      for ip_part, mask_part, dest_part in zip(ip_net, mask_net, dest_ip):
         if dest_part & mask_part != ip_part:
            return False

      return True

   def take_packet(self, packet: dict):
      dest_ip: List[str] = packet['to_ip'].split('.')
      
      for mask i self.ip_table:
         pass
