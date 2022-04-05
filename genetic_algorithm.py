from random import randint
from offspring import Offspring

class GeneticAlgorithm:

    # Constructor
    def __init__(self):
        self.board_size: int = 0
        self.population: list = []
        self.offsprings: list = []
        self.parents: list = []
        self.size: int = 0

    # Enhancing: avoid any repetitions, every position is different form other. Cancels out
    # possibility of having left or right attacks
    def init_pop(self, size: int):
        """
        Initialize population given a size
        :param size: Size of population to init
        :return: void
        """
        self.size = size
        for x in range(self.size):
            child = []
            for z in range(self.board_size):
                pos = randint(1, self.board_size)
                if pos in child:
                    while True:
                        pos = randint(1, self.board_size)
                        if pos not in child:
                            break
                child.append(pos)
            state = Offspring(child)
            state.fitness = self.compute_fitness(state.state)
            self.population.append(state)
        return self.population

    @staticmethod
    # Given a state, calculate it's fitness
    def compute_fitness(state: list):
        """
        Compute fitness of a given state i.e. board
        :param state: N-length list
        :return:
        """
        fitness = 0
        for col in range(len(state)):
            attack = False
            x = state[col]
            for row in range(len(state)):
                diff_col = abs(col - row)
                diff_row = abs(x - state[row])
                if not row == col:
                    # First condition checks for right and left. Second condition checks for
                    # diagonals
                    if x == state[row] or diff_col == diff_row:
                        attack = True
            if not attack: fitness += 1
        return fitness

    # selection done using k-way tournament procedure
    def select_parents(self):
        """
        Select parents using k-way tournament from the given population
        :return:
        """
        self.parents = []
        k = 10  # select 20 states at random
        no_of_parents = int(len(self.population) / 2)
        r_count = 0
        pop_copy = list.copy(self.population)

        for x in range(no_of_parents):
            # select k at random
            tournament = []
            for z in range(k):
                r = randint(0, len(pop_copy) - r_count - 1)
                child = pop_copy[r]
                if child in tournament:
                    while child not in tournament:
                        r = randint(0, len(pop_copy) - r_count - 1)
                        child = pop_copy[r]

                tournament.append(child)
            tournament.sort(reverse=True, key=lambda c: c.fitness)
            winner = tournament.pop(0)
            self.parents.append(winner)
            pop_copy.remove(winner)
            r_count += 1

        return self.parents

    def create_offsprings(self):
        """
        Create offsprings given the parents list in class variable
        :return:
        """
        self.offsprings = []

        divider: int = int(self.board_size / 2)

        p_copy = list.copy(self.parents)

        for i in range(0, len(p_copy)):

            r_1 = randint(0, len(p_copy) - 1)
            r_2 = randint(0, len(p_copy) - 1)
            if r_2 == r_1:
                while not r_2 == r_1:
                    r_2 = randint(0, len(p_copy) - 1)

            p1 = p_copy[r_1]
            p2 = p_copy[r_2]

            if p1 in p_copy: p_copy.remove(p1)
            if p2 in p_copy: p_copy.remove(p2)
            parent_1 = p1.state
            parent_2 = p2.state

            # crossover
            child_1, child_2 = self.crossover(self, parent_1, parent_2, divider)
            # # mutation
            m_child_1 = self.mutation(child_1)
            m_child_2 = self.mutation(child_2)

            c1 = Offspring(m_child_1)
            c1.fitness = self.compute_fitness(m_child_1)
            c2 = Offspring(m_child_2)
            c2.fitness = self.compute_fitness(m_child_2)

            self.offsprings.append(c1)
            self.offsprings.append(c2)

            if len(p_copy) == 0:
                break

        self.population.extend(self.offsprings)

    @staticmethod
    def crossover(self, p1, p2, divider):
        """
        Perform crossover between 2 parents
        :param self:
        :param p1: Parent 1 state for crossover
        :param p2: Parent 2 state for crossover
        :param divider: The divider value which divides a single state, eg. state length = 8,
        divider  = 4
        :return: Return 2 children formed by crossover
        """
        second_half_p1 = p1[divider: self.board_size]
        second_half_p2 = p2[divider: self.board_size]

        child_1 = p1[0: divider] + second_half_p2
        child_2 = p2[0: divider] + second_half_p1

        return child_1, child_2

    def mutation(self, child):
        """
        Perform mutation give a child state.
        :param child: N-length list
        :return: Mutated child
        """
        r = randint(0, len(child) - 1)
        num = child[r]
        while num == self.board_size:
            r = randint(0, len(child) - 1)
            num = child[r]

        binary = bin(num)[2:]
        r_bit = randint(0, len(binary) - 1)
        temp = list(binary)
        temp[r_bit] = self.flip_bit(temp[r_bit])
        x = int(''.join(temp), 2)
        if x <= 0 or x > self.board_size:
            while x <= 0 or x > self.board_size:
                r_bit = randint(0, len(binary) - 1)
                temp = list(binary)
                temp[r_bit] = self.flip_bit(r_bit)
                x = int(''.join(temp), 2)

        child[r] = x
        return child

    @staticmethod
    def flip_bit(bit):
        """
        Flip a given bit
        :param bit:
        :return: flipped bit
        """
        if bit == '1':
            return '0'
        else:
            return '1'

    def kill_members(self):
        """
        Kill redundant members of the population
        :return: None
        """
        to_kill: int = len(self.population) - self.size

        self.population.sort(key=lambda c: c.fitness)
        for x in range(to_kill):
            self.population.remove(self.population[x])

    def genetic_algorithm(self, population_size, board_size, upper_limit, display):
        """
        :param population_size:
        :param board_size:
        :param upper_limit:
        :param display - if true, display all the generations created
        :return: N-queens goal state
        """

        self.board_size = board_size

        self.population = self.init_pop(population_size)

        for x in range(upper_limit):
            self.parents = self.select_parents()
            self.create_offsprings()
            self.kill_members()
            if display:
                print(f'Gen {x}: ')
                for g in self.population: print(g)
            for z in self.population:
                if z.fitness == self.board_size:
                    return z
