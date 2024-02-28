import numpy as np
from queueClient import QueueClient
from task import Task

class Boss(QueueClient):
    def __init__(self):
        super().__init__()

    def assign_task(self, task):
        self.task_queue.put(task)
        print("Task has been assigned")

    def validate_result(self):
        result = self.result_queue.get()
        print("Result received")
        x_vector = result.x
        a_matrix = result.a
        b_vector = result.b
        if np.allclose(np.matmul(a_matrix, x_vector), b_vector):
            return x_vector
        else:
            raise Exception("Result validation failed")

if __name__ == "__main__":
    boss = Boss()
    dimension = 100
    a_matrix = np.random.rand(dimension, dimension)
    b_vector = np.random.rand(dimension, 1)

    boss.assign_task(Task(a_matrix, b_vector))
    x_vector = boss.validate_result()
    print(x_vector)