
from src.model import Model

class Controller:
    def __init__(self):
        self.model = Model()

    def do_something(self):
        # Call a method from the model
        self.model.some_method()

if __name__ ==  "__main__":
    controller = Controller()


