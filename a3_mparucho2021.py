"""
    Author: Marco Parucho
    Date: 07/01/2023
    Description: Creating a solution to the Traveling Salesman Problem
    using colony optimization. Code based on algorithms provided in textbook.
"""
import random
import math 
import numpy as np # will need to use this library to be able to show a graph to an user.
import matplotlib.pyplot as plt

N = 25 #Number of cities, keep to 25 for default. You can play around with it to see others paths. Please stay between 1-100.

random.seed(40) #you can change the random seed to see different paths 

#Generating random points for the cities
cities = [(random.uniform(0, 200), random.uniform(0, 200)) for _ in range(N)]

#Encapsulating the basic logic for an ant
class Ant:
    def __init__(self, attraction_count):
        self.visited_attractions = []
        self.attraction_count = attraction_count

    def visit_attractions(self, pheromone_trails, alpha, beta):
        if random.random() < 0.5:
            self.visit_random_attraction()
        else:
            self.visit_probabilistic_attraction(pheromone_trails, alpha, beta)

    def visit_random_attraction(self):
        attraction = random.randint(0, self.attraction_count - 1)
        self.visited_attractions.append(attraction)
    #this function deals with the probabilty of an ant visiting a city. Close to heuristics.
    def visit_probabilistic_attraction(self, pheromone_trails, alpha, beta):
        current_attraction = self.visited_attractions[-1]
        all_attractions = list(range(self.attraction_count))
        possible_attractions = list(set(all_attractions) - set(self.visited_attractions))

        possible_indexes = []
        possible_probabilities = []
        total_probabilities = 0

        for attraction in possible_attractions:
            possible_indexes.append(attraction)
            pheromones_on_path = math.pow(pheromone_trails[current_attraction][attraction], alpha)
            distance = math.sqrt((cities[current_attraction][0] - cities[attraction][0]) ** 2 +
                                 (cities[current_attraction][1] - cities[attraction][1]) ** 2)
            probability = pheromones_on_path * (1 / distance) ** beta
            possible_probabilities.append(probability)
            total_probabilities += probability

        if total_probabilities == 0:
            num_possible_attractions = len(possible_attractions)
            equal_prob = 1 / num_possible_attractions
            return [possible_indexes, [equal_prob] * num_possible_attractions]

        possible_probabilities = [probability / total_probabilities for probability in possible_probabilities]
        return [possible_indexes, possible_probabilities]
    
    def get_distance_traveled(self):
        total_distance = 0
        for a in range(1, len(self.visited_attractions)):
            previous_attraction = self.visited_attractions[a - 1]
            current_attraction = self.visited_attractions[a]
            distance = math.sqrt((cities[previous_attraction][0] - cities[current_attraction][0]) ** 2 +
                                 (cities[previous_attraction][1] - cities[current_attraction][1]) ** 2)
            total_distance += distance
        return total_distance

#this function setes up the colony of ants. It appends them to a list to keep track of by reference.
def setup_ants(attraction_count, number_of_ants_factor):
    number_of_ants = round(attraction_count * number_of_ants_factor)
    ant_colony = []

    for _ in range(number_of_ants):
        ant = Ant(attraction_count)
        ant.visit_random_attraction()
        ant_colony.append(ant)
    return ant_colony


def move_ants(ant_colony, pheromone_trails, alpha, beta):
    for ant in ant_colony:
        ant.visit_attractions(pheromone_trails, alpha, beta)

#updating pheromone trails
def update_pheromones(evaporation_rate, pheromone_trails, ant_colony):
    for x in range(N):
        for y in range(N):
            pheromone_trails[x][y] *= evaporation_rate

    for ant in ant_colony:
        distance_traveled = ant.get_distance_traveled()
        if distance_traveled > 0:
            for a in range(1, len(ant.visited_attractions)):
                previous_attraction = ant.visited_attractions[a - 1]
                current_attraction = ant.visited_attractions[a]
                pheromone_trails[previous_attraction][current_attraction] += 1 / distance_traveled

    return pheromone_trails

#retraving the best ant from the population
def get_best(ant_population, previous_best_ant):
    best_ant = previous_best_ant
    for ant in ant_population:
        if ant.get_distance_traveled() < best_ant.get_distance_traveled():
            best_ant = ant
    return best_ant

#Putting everything together, Solving TSP with ACO
def solve(total_iterations, evaporation_rate, number_of_ants_factor, alpha, beta):
    pheromone_trails = np.ones((N, N))
    ant_colony = setup_ants(N, number_of_ants_factor)
    best_ant = ant_colony[0]

    for _ in range(total_iterations):
        for ant in ant_colony:
            ant.visited_attractions = []
            ant.visit_random_attraction()

        for _ in range(N - 1):
            move_ants(ant_colony, pheromone_trails, alpha, beta)

        update_pheromones(evaporation_rate, pheromone_trails, ant_colony)

        best_ant = get_best(ant_colony, best_ant)

    return best_ant


#settings...
total_iterations = 100
evaporation_rate = 0.5
number_of_ants_factor = 0.8
alpha = 1
beta = 2

best_ant = solve(total_iterations, evaporation_rate, number_of_ants_factor, alpha, beta)

#Print the path of cities visited by the best ant
city_path = [cities[i] for i in best_ant.visited_attractions]
city_names = [f"City {i + 1}: {city}" for i, city in zip(best_ant.visited_attractions, city_path)]
print("Path of Cities:", ", ".join(city_names))

#Plot the cities and the best path
x_coords = [city[0] for city in cities]
y_coords = [city[1] for city in cities]

#Plot the cities
plt.scatter(x_coords, y_coords, color='b', label='Cities')

#Plot the best path
plt.plot(x_coords, y_coords, color='gray', linestyle='--')
plt.plot(x_coords, y_coords, color='r', linestyle='-', linewidth=1.5)

#Scatter plot for the best path (to make it visible)
plt.scatter(x_coords, y_coords, color='r', label='Best Path')

#Scatter plot for the starting city
plt.scatter(x_coords[0], y_coords[0], color='g', label='Starting City')

#displaying to the user
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Traveling Salesman Problem Solution by Marco Parucho')
plt.legend()
plt.grid(True)
plt.show()
