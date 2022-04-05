"""
Ali Ahmed Nadeem - 23017
pip install pygame
"""
from visualize import visualize_board
from genetic_algorithm import GeneticAlgorithm

# if True, displays the final goal state in a pygame window.
# if False, prints the goal state on command line
draw_board = False

ga = GeneticAlgorithm()

"""
Run genetic algorithm for the N-queen problem
:param: Population size : int
:param: board_size: int - the no. of queens on a board i.e. N x N
:param: upper_limit: int - the max no. of iterations to be done in the genetic algorithm
:param: display: boolean - If passed true, shows every generation created in every iteration 
Ideal population size needs to be a large value for better results
"""
goal_state = ga.genetic_algorithm(500, 8, 500, False)
print(goal_state)

if goal_state is not None:
    if draw_board:
        visualize_board(goal_state.state)






