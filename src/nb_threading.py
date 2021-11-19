import threading
import time
import logging
import uuid
import typing


class nlThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self, function, *args, **kwargs):
      # Get lock to synchronize threads
      threadLock.acquire()
      function(*args, **kwargs)
      # Free lock to release next thread
      threadLock.release()

class nlThreadHandler:
   def __init__(self, function, no_of_threads : int, function_input_size : int, args):
      self.function = function
      self.thread_handler_ID = uuid.uuid4()
      self.no_of_threads = no_of_threads
      self.function_input_size = function_input_size

   def run(self):
      pass

   def __del__(self):
      pass
