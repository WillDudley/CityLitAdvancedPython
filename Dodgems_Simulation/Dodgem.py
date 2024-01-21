import copy

import numpy as np


class Dodgem:
    def __init__(self, hit_points, policy, speed, initial_location, dodgem_id, arena_size):
        self.hit_points = hit_points
        self.policy = policy
        self.speed = speed
        self.current_location = initial_location
        self.next_location = initial_location
        self.dodgem_id = dodgem_id
        self.arena_size = arena_size

        self.alive = True

    def step(self, all_dodgems):
        if self.policy == "SE":
            normed_action = np.array([1, 1]) / np.sqrt(2)

        elif self.policy == "Random":
            normed_action = np.random.randint(low=-1, high=2, size=2) / np.sqrt(2)

        elif self.policy == "Pursuit":
            dodgem_id_to_pursue = self._calculate_closest_dodgem(all_dodgems)
            normed_action = self._calculate_vector_towards_dodgem(dodgem_id_to_pursue)

        elif self.policy == "Escape":
            dodgem_id_to_pursue = self._calculate_closest_dodgem(all_dodgems)
            normed_action = -self._calculate_vector_towards_dodgem(dodgem_id_to_pursue)
        else:
            raise ValueError(f"Dodgem {self.dodgem_id}'s policy of '{self.policy}' not recognised!")

        self.next_location += np.rint((normed_action * self.speed) / np.sqrt(2)).astype(np.int32)

        print(f"Dodgem {self.dodgem_id} took action {np.rint((normed_action * self.speed) / np.sqrt(2)).astype(np.int32)}")

        # account for collision with wall
        for i in [0, 1]:
            if self.next_location[i] >= self.arena_size:
                self.next_location[i] -= self.speed  # walls bounce dodgems back by their speed
            elif self.next_location[i] < 0:
                self.next_location[i] += self.speed

        self.current_location = copy.copy(self.next_location)

    def decrement_hp(self):
        self.hit_points -= 1
        print(f"Dodgem {self.dodgem_id} hit! Remaining HP: {self.hit_points}")
        if self.hit_points <= 0:
            self.alive = False
            self.current_location = None
            print(f"Dodgem {self.dodgem_id} destroyed!")

    def _calculate_closest_dodgem(self, all_dodgems):
        current_max_dist = np.inf
        for dodgem in all_dodgems:
            if dodgem.alive and dodgem.dodgem_id != self.dodgem_id:
                distance = np.linalg.norm(self.current_location - dodgem.current_location)
                if distance < current_max_dist:
                    current_max_dist = distance
                    closest_dodgem = dodgem
        return closest_dodgem

    def _calculate_vector_towards_dodgem(self, dodgem):
        relative_vector = dodgem.current_location - self.current_location
        if relative_vector.any():
            normed_vector = relative_vector / np.linalg.norm(relative_vector)
        else:
            normed_vector = relative_vector
        return normed_vector
