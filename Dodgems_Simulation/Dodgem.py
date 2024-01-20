import numpy as np


class Dodgem:
    def __init__(self, hit_points, speed, pursuit_strategy, current_location, dodgem_id):
        self.hit_points = hit_points
        self.speed = speed
        self.pursuit_strategy = pursuit_strategy
        self.alive = True
        self.current_location = current_location
        self.dodgem_id = dodgem_id

    def step(self):
        if self.alive:
            self.current_location += np.array([1, 1])
        else:
            self.current_location = None

    def _check_collision(self):
        pass

    def _update_velocity(self):
        pass

    def _check_alive(self):
        pass
