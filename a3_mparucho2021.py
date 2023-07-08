"""
    Author: Marco Parucho
    Date: 07/01/2023
    Description: Creating a solution to the Traveling Salesman Problem
    using colony optimization. Code based on algorithms provided in textbook.
"""
import random
import math

# This matrix represents the distance between entities
d_matrix = [
    [0, 8, 7, 4, 6, 4],
    [8, 0, 5, 7, 11, 5],
    [7, 5, 0, 9, 6, 7],
    [4, 7, 9, 0, 5, 6],
    [6, 11, 6, 5, 0, 3],
    [4, 5, 7, 6, 3, 0]
]

# Encapsulating the basic logic for an ant
class Ant:
    def __init__(self, attraction_count):
        self.visited_attractions = []
        self.attraction_count = attraction_count

    def visit_attractions(self, pheromone_trails):
        if random.random() < 0.5:
            self.visit_random_attraction()
        else:
            self.visit_probabilistic_attraction(pheromone_trails)

    def visit_random_attraction(self):
        attraction = random.randint(0, self.attraction_count - 1)
        self.visited_attractions.append(attraction)

    def visit_probabilistic_attraction(self, pheromone_trails):
        # Implementation goes here
        pass

    def get_distance_traveled(self):
        total_distance = 0
        for a in range(1, len(self.visited_attractions)):
            previous_attraction = self.visited_attractions[a - 1]
            current_attraction = self.visited_attractions[a]
            total_distance += d_matrix[previous_attraction][current_attraction]
        return total_distance


# Declaring a matrix that will represent the intensity of the pheromones on the path
pheromone_trails = [[1] * len(d_matrix) for _ in range(len(d_matrix))]

# This function sets up the colony of ants. It appends them to a list to keep track of by reference.
def setup_ants(attraction_count, number_of_ants_factor):
    number_of_ants = round(attraction_count * number_of_ants_factor)
    ant_colony = []

    for i in range(number_of_ants):
        ant = Ant(attraction_count)
        ant.visit_random_attraction()
        ant_colony.append(ant)
    return ant_colony

# This function calculates the probability of visiting a city
def visit_probabilistic_attraction(pheromone_trails, attraction_count, ant, alpha, beta):
    current_attraction = ant.visited_attractions[-1]
    all_attractions = list(range(attraction_count))
    possible_attractions = list(set(all_attractions) - set(ant.visited_attractions))

    possible_indexes = []
    possible_probabilities = []
    total_probabilities = 0

    for attraction in possible_attractions:
        possible_indexes.append(attraction)
        pheromones_on_path = math.pow(pheromone_trails[current_attraction][attraction], beta)
        heuristic_for_path = 1 / d_matrix[current_attraction][attraction]
        probability = pheromones_on_path * heuristic_for_path
        possible_probabilities.append(probability)
        total_probabilities += probability

    if total_probabilities == 0:
        num_possible_attractions = len(possible_attractions)
        equal_prob = 1 / num_possible_attractions
        return [possible_indexes, [equal_prob] * num_possible_attractions]

    possible_probabilities = [probability / total_probabilities for probability in possible_probabilities]
    return [possible_indexes, possible_probabilities]



# This function performs roulette wheel selection
def roulette_wheel_selection(possible_indexes, possible_probabilities, possible_attractions_count):
    slices = []
    total = 0

    for i in range(possible_attractions_count):
        slice_range = [possible_indexes[i], total, total + possible_probabilities[i]]
        slices.append(slice_range)
        total += possible_probabilities[i]

    spin = random.uniform(0, 1)
    result = [slice_range for slice_range in slices if slice_range[1] < spin <= slice_range[2]]

    return result

# This function updates the pheromone trails
def update_pheromones(evaporation_rate, pheromone_trails, attraction_count, ant_colony):
    for x in range(attraction_count):
        for y in range(attraction_count):
            pheromone_trails[x][y] *= evaporation_rate

    for ant in ant_colony:
        distance_traveled = ant.get_distance_traveled()
        if distance_traveled > 0:
            for x in range(attraction_count):
                for y in range(attraction_count):
                    pheromone_trails[x][y] += 1 / distance_traveled

    return pheromone_trails

# This function retrieves the best ant from the ant population
def get_best(ant_population, previous_best_ant):
    best_ant = previous_best_ant
    for ant in ant_population:
        if ant.get_distance_traveled() < best_ant.get_distance_traveled():
            best_ant = ant
    return best_ant

# This function controls the movement of ants in each iteration
def move_ants(ant_colony, pheromone_trails, attraction_count, alpha, beta):
    for ant in ant_colony:
        ant.visit_attractions(pheromone_trails)

# This function solves the TSP using ACO
def solve(total_iterations, evaporation_rate, number_of_ants_factor, attraction_count, alpha, beta):
    pheromone_trails = [[1] * attraction_count for _ in range(attraction_count)]
    ant_colony = setup_ants(attraction_count, number_of_ants_factor)
    best_ant = ant_colony[0]  # Initialize with the first ant in the colony

    for i in range(total_iterations):
        for ant in ant_colony:
            ant.visited_attractions = []  # Reset visited attractions for each ant
            ant.visit_random_attraction()  # Start with a random attraction

        for r in range(attraction_count - 1):
            move_ants(ant_colony, pheromone_trails, attraction_count, alpha, beta)

        update_pheromones(evaporation_rate, pheromone_trails, attraction_count, ant_colony)

        best_ant = get_best(ant_colony, best_ant)

    return best_ant


#Calling the program
total_iterations = 200
evaporation_rate = 0.5
number_of_ants_factor = 0.8
attraction_count = len(d_matrix)
alpha = 1  # Define the value for alpha
beta = 2  # Define the value for beta

best_ant = solve(total_iterations, evaporation_rate, number_of_ants_factor, attraction_count, alpha, beta)

# Print the best ant and its distance traveled
print("Best Ant:", best_ant.visited_attractions)
print("Distance Traveled:", best_ant.get_distance_traveled())
