'''
Описывает генерацию заданий и взаимодействие с заказчиками
'''
from typing import List
from datetime import datetime
from dataclasses import dataclass
from .data import *


@dataclass
class Task:
   herz: int
   paral_degree: float
   storage_mem: int
   deadline: datetime
   task_type: str

   def generate_data(self) -> bytes:
      if self.task_type:
         div = 2
         while self.storage_mem / div != 0:
            div += 1

         csv_data: str = create_csv(div, self.storage_mem // div)
         return bytes(csv_data, 'utf-8')

   def generate_single(self) -> None:
      pass



class Stock:
   def __init__(self, players=1):
      self.players: int = players
      self.tasks: List[Task] = []


   def generate_tasks(self):
      for i in range(len(self.tasks), 10*self.players):
         self.tasks.append(Task(herz=i*42000000,
                                 paral_degree=0.,
                                 storage_mem=(i**2)*120*1024,
                                 deadline=datetime.now(),
                                 task_type='csv'))

