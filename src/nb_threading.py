import threading
import time
import uuid

class nlReturnValueThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target is None:
            return  # could alternatively raise an exception, depends on the use case
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)  # properly handle the exception

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result

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
