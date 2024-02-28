import multiprocessing as mp
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    def __init__(self, address, authkey): #adress is a tuple (ip, port)
        super().__init__(address, authkey)
        self.task_queue = mp.Queue()
        self.result_queue = mp.Queue()

        self.register('get_taks_queue', callable=lambda: self.task_queuequeue)
        self.register('get_result_queue', callable=lambda: self.result_queue)

    def launch(self):
        self.get_server().serve_forever()

if __name__ == "__main__":
    address = ('localhost', 50000)
    authkey = b'authkey'
    manager = QueueManager(address, authkey)
    manager.launch()

