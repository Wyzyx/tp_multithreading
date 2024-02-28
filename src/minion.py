from queueClient import QueueClient
from task import Task

class Minion(QueueClient):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            task = self.get_task(self.task_queue)
            print(f"Minion received task: {task}")
            result = task.run()
            self.result_queue.put(result)
    
    if __name__ == "__main__":
        minion = Minion()
        minion.run()