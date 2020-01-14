##############################
# Particle Swarm Algorithm
# by Piotr Pasterak
# December 2019
###############################

import random
from math import sin, cos, sqrt, atan2, radians, exp
import json


###############################
# Constants
INERTIA_WEIGHT = 0.6
IND_FOCUS_CONSTANT = 1
SWARM_FOCUS_CONSTANT = 4
DIMENSIONS = 30
POSITION_RANGE = [1, 30]
VELOCITY_RANGE = [-10, 10]
CAPACITY = 1000
###############################

# approximate radius of earth in km
R = 6373.0


def calculate_distance(latitude_source, longitude_source, latitude_destination, longitude_destination):
    source_radians_latitude = radians(latitude_source)
    source_radians_longitude = radians(longitude_source)

    destination_radians_latitude = radians(latitude_destination)
    destination_radians_longitude = radians(longitude_destination)

    dlon = destination_radians_longitude - source_radians_longitude
    dlat = destination_radians_latitude - source_radians_latitude

    a = sin(dlat / 2)**2 + cos(source_radians_latitude) * cos(destination_radians_latitude) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def sigmoid(x):
    return 1 / (1 + exp(-x))


def goal_function(positions):
    travel_sum = 0
    temp_pos=[]
    idx =0

    for i in positions:
        temp_pos.append((idx, i))
        idx += 1

    temp_pos.sort(key = lambda item: item[1])

    with open('data/cites.json', encoding="utf8") as json_file:
        data = json.load(json_file)

        base = data["cites"][0]
        length = len(temp_pos)
        i = 1 #KRK is 0
        car_capacity = 0

        while i < length:
            if car_capacity == 0:
                travel_sum += calculate_distance(base["latitude"], base["longitude"],
                                               data["cites"][temp_pos[i][0]+1]["latitude"], data["cites"][temp_pos[i][0]+1]["longitude"])
                car_capacity += data["cites"][temp_pos[i][0]+1]["demand"]
                i += 1
            else:
                if i+1 == length or car_capacity + data["cites"][temp_pos[i + 1][0] + 1]["demand"] > CAPACITY:
                    travel_sum += calculate_distance(data["cites"][temp_pos[i][0] + 1]["latitude"],
                                                     data["cites"][temp_pos[i][0] + 1]["longitude"],
                                                     base["latitude"], base["longitude"])
                    car_capacity = 0
                else:
                    travel_sum += calculate_distance(data["cites"][temp_pos[i][0]+1]["latitude"], data["cites"][temp_pos[i][0]+1]["longitude"],
                                             data["cites"][temp_pos[i+1][0] + 1]["latitude"], data["cites"][temp_pos[i+1][0] + 1]["longitude"])
                    car_capacity += data["cites"][temp_pos[i][0] + 1]["demand"]
                    i += 1

    return travel_sum, temp_pos


def decode_travel(positions):
    travel = []
    with open('data/cites.json', encoding="utf8") as json_file:
        data = json.load(json_file)

        base = data["cites"][0]
        length = len(positions)
        i = 1  # KRK is 0
        car_capacity = 0

        while i < length:
            if car_capacity == 0:
                travel.append(base["city_name"])
                travel.append( data["cites"][positions[i][0] + 1]["city_name"])

                car_capacity += data["cites"][positions[i][0] + 1]["demand"]
                i += 1
            else:
                if i + 1 == length or car_capacity + data["cites"][positions[i + 1][0] + 1]["demand"] > CAPACITY:
                    travel.append(data["cites"][positions[i][0] + 1]["city_name"])
                    travel.append(base["city_name"])
                    car_capacity = 0
                    i += 1
                else:
                    travel.append(data["cites"][positions[i][0] + 1]["city_name"])
                    car_capacity += data["cites"][positions[i][0] + 1]["demand"]
                    i += 1
    return travel


class Particle:
    def __init__(self):
        self.position = []
        self.velocity = []
        self.best_position = {}
        self.best_distance = -1
        self.distance = -1

        self.init_position()
        self.init_velocity()

    def init_position(self):
        for i in range(0, DIMENSIONS):
            self.position.append(random.uniform(POSITION_RANGE[0], POSITION_RANGE[1]))

    def init_velocity(self):
        for i in range(0, DIMENSIONS):
            self.velocity.append(random.uniform(VELOCITY_RANGE[0], VELOCITY_RANGE[1]))

    def evaluate_fitness(self):
        self.distance, _ = goal_function(self.position)

        if self.distance < self.distance or self.best_distance == -1:
            self.best_position = self.position
            self.best_distance = self.distance

    def update_velocity(self, best_swarm_position):

        for i in range(0, DIMENSIONS):
            random_coefficient = random.random()
            velocity_ind_focus_part = IND_FOCUS_CONSTANT * random_coefficient * (self.best_position[i] - self.position[i])
            random_coefficient = random.random()
            velocity_swarm_focus_part = SWARM_FOCUS_CONSTANT * random_coefficient * (best_swarm_position[i] - self.position[i])
            self.velocity[i] = INERTIA_WEIGHT * self.velocity[i] + velocity_ind_focus_part + velocity_swarm_focus_part

    def update_position(self):
        for i in range(0, DIMENSIONS):
            self.position[i] = self.position[i] + self.velocity[i]

            # adjust maximum position if necessary
            if self.position[i] > POSITION_RANGE[1]:
                self.position[i] = POSITION_RANGE[1] * sigmoid(self.position[i])

            # adjust minimum position if necessary
            if self.position[i] < POSITION_RANGE[0]:
                self.position[i] = POSITION_RANGE[0] * sigmoid(self.position[i])

    def evaluate_step(self, best_group_position):
        self.evaluate_fitness()
        self.update_velocity(best_group_position)
        self.update_position()

        return self.best_position, self.best_distance


class Swarm:
    def __init__(self, particles_num, iterations_num):
        self.best_swarm_distance = -1
        self.best_swarm_position = []
        self.iter_num = iterations_num
        self.particle_swarm = [Particle() for x in range(0, particles_num)]

    def calculate(self):
        for i in range(0, self.iter_num):
            for particle in self.particle_swarm:
                particle.evaluate_fitness()

                if particle.best_distance < self.best_swarm_distance or self.best_swarm_distance == -1:
                    self.best_swarm_distance = particle.best_distance
                    self.best_swarm_position = particle.best_position

            for particle in self.particle_swarm:
                particle.evaluate_step(self.best_swarm_position)


if __name__ == '__main__':
    test_swarm = Swarm(60, 150)
    test_swarm.calculate()
    print(str(test_swarm.best_swarm_distance) + "\n")
    _, best_travel = goal_function(test_swarm.best_swarm_position)
    print(best_travel)
    print(decode_travel(best_travel))

