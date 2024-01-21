import numpy as np


class Dodgem:
    def __init__(self, hit_points, speed, pursuit_strategy, current_location, dodgem_id, arena_size):
        self.hit_points = hit_points
        self.speed = speed
        self.pursuit_strategy = pursuit_strategy
        self.alive = True
        self.current_location = current_location
        self.dodgem_id = dodgem_id
        self.arena_size = arena_size

    def step(self):
        self.current_location += np.array([1, 1])

        # account for collision with wall
        for i in [0, 1]:
            if self.current_location[i] >= self.arena_size:
                self.current_location[i] -= 1
            elif self.current_location[i] < 0:
                self.current_location[i] += 1

    def decrement_hp(self):
        self.hit_points -= 1
        if self.hit_points <= 0:
            self.alive = False
            self.current_location = None
            print(f"Dodgem {self.dodgem_id} destroyed!")
