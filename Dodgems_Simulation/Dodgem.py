import numpy as np


class Dodgem:
    def __init__(self, hit_points, policy, initial_location, dodgem_id, arena_size):
        self.hit_points = hit_points
        self.policy = policy
        self.alive = True
        self.current_location = initial_location
        self.dodgem_id = dodgem_id
        self.arena_size = arena_size

    def step(self, all_dodgems):
        if self.policy == "SE":
            self.current_location += np.array([1, 1])
        elif self.policy == "Random":
            self.current_location += np.random.randint(low=-1, high=1, size=2)
        elif self.policy == "Pursuit":
            pass
        elif self.policy == "Escape":
            pass
        else:
            raise ValueError(f"Dodgem {self.dodgem_id}'s policy of '{self.policy}' not recognised!")

        # account for collision with wall
        for i in [0, 1]:
            if self.current_location[i] >= self.arena_size:
                self.current_location[i] -= 1
            elif self.current_location[i] < 0:
                self.current_location[i] += 1

    def decrement_hp(self):
        self.hit_points -= 1
        print(f"Dodgem {self.dodgem_id} hit! Remaining HP: {self.hit_points}")
        if self.hit_points <= 0:
            self.alive = False
            self.current_location = None
            print(f"Dodgem {self.dodgem_id} destroyed!")
