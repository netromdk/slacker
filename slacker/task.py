from abc import ABC, abstractmethod

from concurrent.futures import ProcessPoolExecutor

class Task(ABC):
  @abstractmethod
  def run():
    pass

def start_task(task):
  return task.run()

def execute_tasks(tasks):
  pool = ProcessPoolExecutor()
  return pool.map(start_task, tasks)
