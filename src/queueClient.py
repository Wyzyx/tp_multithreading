import multiprocessing as mp

from queueManager import QueueManager
from task import Task

class QueueClient:
    def __init__(self):
        self.queue_manager = QueueManager(address=('localhost', 50000), authkey=b'1234')
        self.queue_manager.connect()

        self.queue_manager.register('get_task_queue')
        self.task_queue = self.queue_manager.get_task_queue()

        self.queue_manager.register('get_result_queue')
        self.result_queue = self.queue_manager.get_result_queue()

    def get_task(self, queue) -> Task:
        return queue.get()

    if __name__ == "__main__":
        queue_client = QueueClient()
        print("queue client running with queue :", queue_client.task_queue)


        
