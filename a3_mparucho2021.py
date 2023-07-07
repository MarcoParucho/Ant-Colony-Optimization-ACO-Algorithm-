"""
    Author: Marco Parucho
    Date:07/01/2023
    Description: Creating a solution to the Traveling Salesman Problem
    using colony optimization. Code based on algorithms provided in textbook.
"""
import random

#this matrix represents the distance between  entities
d_matrix = [
   [0, 8, 7, 4, 6, 4],
   [8, 0, 5, 7, 11, 5],
   [7, 5, 0, 9, 6, 7],
   [4, 7, 9, 0, 5, 6],
   [6, 11, 6, 5, 0, 3],
   [4, 5, 7, 6, 3, 0]
]

#encapsulating the basic logic for an ant
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

    def get_distance_traveled(ant):
        total_distance = 0
        
        for a in range(1, len(ant.visited_attractions)):
            previous_attraction = ant.visited_attractions[a-1]
            current_attraction = ant.visited_attractions[a]
            total_distance += d_matrix[previous_attraction][current_attraction]
        return total_distance

#Declaring a matrix that will represent the intersity of the pheromones on the path 
pheromone_trails = [
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
]

#this function sets up the colony of ants. It appends them to a list to keep track of by reference
def setup_ants(attraction_count, number_of_ants_factor):
    number_of_ants = round(attraction_count*number_of_ants_factor)
    ant_colony = []

    for i in range(number_of_ants):
        ant = Ant(attraction_count)
        ant.visit_random_attraction()
        ant_colony.append(ant)
    return ant_colony


