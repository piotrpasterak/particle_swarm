##############################
# Particle Swarm Algorithm
# by Piotr Pasterak
# December 2019
###############################

import random

###############################
# Constants
INERTIA_WEIGHT = 0.5
IND_FOCUS_CONSTANT = 1
SWARM_FOCUS_CONSTANT = 2
DIMENSIONS = 2
POSITION_RANGE = [-100, 100]
VELOCITY_RANGE = [-10, 10]
###############################

def goal_function(position):
    return 0


class Particle:
    def __init__(self):
        self.position = []
        self.velocity = []
        self.best_position = []
        self.best_distance = -1
        self.distance = -1

        self.init_position()
        self.init_velocity()

    def init_position(self):
        for i in range(0, DIMENSIONS):
            self.position.append(random.uniform(POSITION_RANGE[0], POSITION_RANGE[1]))

    def init_velocity(self):
        for i in range(0, DIMENSIONS):
            self.velocity.append(random.uniform(VELOCITY_RANGE[0] , VELOCITY_RANGE[1]))

    def evaluate_fitness(self):
        self.distance = goal_function(self.position)

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
            if self.position_i[i]>POSITION_RANGE[1]:
                self.position_i[i]=POSITION_RANGE[1]

            # adjust minimum position if neseccary
            if self.position_i[i] < POSITION_RANGE[0]:
                self.position_i[i]=POSITION_RANGE[0]

    def evaluate_step(self, best_group_position):
        self.evaluate_fitness()
        self.update_velocity(best_group_position)
        self.update_velocity()

        return self.best_position, self.best_distance


class Swarm:
    def __init__(self, particles_num, iterations_num):
        self.best_swarm_distance = -1
        self.best_swarm_position = []
        self.iter_num = iterations_num
        self.particle_swarm = [Particle() for x in range(0, particles_num)]

    def calculate(self, iterations_num):
        for i in range(0, iterations_num):
            for particle in self.swarm:
                particle.evaluate_fitness()

                if particle.best_distance < self.best_swarm_distance or self.best_swarm_distance == -1:
                    self.best_swarm_distance = particle.best_distance
                    self.best_swarm_position = particle.best_position

            for particle in self.swarm:
                particle.evaluate_step(self.best_swarm_position)


if __name__ == '__main__':
    test_swarm = Swarm(100,30)
    print(test_swarm.best_swarm_distance + "\n")
    print(test_swarm.best_swarm_position)

