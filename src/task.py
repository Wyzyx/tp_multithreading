import time
import json
import numpy as np


class Task:
    def __init__(self, identifier):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def to_json(self) -> str:
        """
        Create a JSON string from the task
        Use custom encoder to serialize NumPy arrays
        """
        class TaskEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return json.JSONEncoder.default(self, obj)

        return TaskEncoder().encode(self.__dict__)

    @classmethod
    def from_json(cls, text: str):
        data = json.loads(text)
        return cls(data["a"], data["b"], data["identifier"], data["x"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False

        return (
            self.identifier == other.identifier
            and np.array_equal(self.a, other.a)
            and np.array_equal(self.b, other.b)
            and np.array_equal(self.x, other.x)
        )

    def __str__(self) -> str:
        return (
            f"Task {self.identifier}:\n"
            f"a:\n{self.a}\n"
            f"b:\n{self.b}\n"
            f"x:\n{self.x}\n"
        )


if __name__ == "__main__":
    print("=== Test work ===")
    size = 5
    a = np.random.rand(size, size)
    b = np.random.rand(size, 1)

    task = Task(a, b)
    x = task.work()
    print("Check:", np.allclose(a @ x, b))

    print("=== Test serialization ===")
    task = Task(a, b)
    print(task)
    s_json = task.to_json()
    print(s_json)
    task2 = Task.from_json(s_json)
    print(task2)

    print("Check is equal:", task == task2)