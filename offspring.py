class Offspring:

    def __init__(self, state: list):
        self.state = state
        self.fitness = None

    def __str__(self):
        return f'State: {self.state} | Fitness: {self.fitness}'
