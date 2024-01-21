import numpy as np
from Dodgem import Dodgem
from collections import defaultdict


class Arena:
    def __init__(self, arena_size, n_dodgems, dodgem_policies, dodgem_hitpoints, time_limit=10_000, render=True):
        self.arena_size = arena_size
        self.n_dodgems = n_dodgems
        self.dodgem_policies = dodgem_policies
        self.dodgem_hitpoints = dodgem_hitpoints
        self.time_limit = time_limit
        self.render = render

        self.dodgems = []  # Create empty list that will hold the dodgems objects
        self.terminated = False
        self.time_step = 0
        self.alive_dodgems = []

        for i in list(range(n_dodgems)):
            self.add_dodgem(i + 1)

        self._render()

    def step(self):
        # Move dodgems if they are alive
        for dodgem in self.dodgems:
            if dodgem.alive:

                dodgem.step()

        self._check_collision_between_dodgems()

        if self.render:
            test_alive_dodgems_sync_with_arena_render(self._render(), self.dodgems)

        # Plot

        # termination check
        self.time_step += 1
        self._check_terminal()

    def add_dodgem(self, dodgem_id, random_start=True):
        """
        Create a new dodgem, add it to the list of dodgems, and place it in a random square in the arena
        :return:
        """

        if random_start:
            # Logic to check we are not adding a dodgem on top of another dodgem
            dodgem_unassigned = True

            while dodgem_unassigned:
                x_coordinate, y_coordinate = np.random.randint(0, self.arena_size, 2)
                dodgem_conflict = False
                for dodgem in self.dodgems:
                    if x_coordinate == dodgem.current_location[0] and y_coordinate == dodgem.current_location[1]:
                        dodgem_conflict = True
                if not dodgem_conflict:
                    dodgem_unassigned = False
        else:
            x_coordinate = -dodgem_id % self.arena_size
            y_coordinate = dodgem_id  # % self.arena_size

        assert 0 <= x_coordinate < self.arena_size, f"Initial x coordinate for dodgem {dodgem_id} out of bounds!"
        assert 0 <= y_coordinate < self.arena_size, f"Initial y coordinate for dodgem {dodgem_id} out of bounds!"

        self.dodgems.append(Dodgem(hit_points=self.dodgem_hitpoints[dodgem_id-1],
                                   policy=self.dodgem_policies[dodgem_id-1],
                                   initial_location=np.array([x_coordinate, y_coordinate]),
                                   dodgem_id=dodgem_id,
                                   arena_size=self.arena_size))
        self.alive_dodgems.append(dodgem_id)

    def _plot(self):
        pass

    def _render(self):
        arena = np.zeros((self.arena_size, self.arena_size))

        for dodgem in self.dodgems:
            if dodgem.alive:
                if arena[dodgem.current_location[0], dodgem.current_location[1]] != 0:  # if a dodgem is already in the location...
                    arena[dodgem.current_location[0], dodgem.current_location[1]] = -1  # just replace it with -1
                else:
                    arena[dodgem.current_location[0], dodgem.current_location[1]] = dodgem.dodgem_id

        print(arena)
        return arena

    def _check_terminal(self):
        if len(self.alive_dodgems) <= 1:
            self.terminated = True
            print(f"Simulation terminated as there are {len(self.alive_dodgems)} dodgem(s) remaining!")
        elif self.time_step >= self.time_limit:
            self.terminated = True
            print(f"Simulation terminated as the time exceeded the limit of {self.time_limit} steps!")

    def _check_collision_between_dodgems(self):
        # Assess for collisions by looking at the coordinates of all alive dodgems, checking for overlaps
        coordinate_list = [tuple(dodgem.current_location) if dodgem.alive else None for dodgem in self.dodgems]

        for index, collision_coord in list_duplicates(coordinate_list):  # https://stackoverflow.com/a/5419576
            # If the dodgem is where another dodgem is, damage it
            self.dodgems[index].decrement_hp()
            if not self.dodgems[index].alive:
                self.alive_dodgems.remove(self.dodgems[index].dodgem_id)


def list_duplicates(seq):  # https://stackoverflow.com/a/5419576
    """

    :param seq: list of coordinates
    :return: list of duplicates in the format [(index, duplicate_element), ...]
    """
    duplicates = []
    for i in list(range(len(seq))):
        if seq[i] is None:
            continue  # ignore dead dodgems
        for j in list(range(len(seq))):
            if i != j:
                if seq[i] == seq[j]:
                    duplicates.append((i, seq[i]))
    return set(duplicates)  # when >2 dodgems are destroyed simultaneously, duplicates of this list are made


def test_alive_dodgems_sync_with_arena_render(arena: np.array, dodgems_list: list[Dodgem]):
    # I could use itertools or zip() here but I'm not confident enough
    list_of_alive_dodgems_shown = []

    for row in arena:
        for number_displayed in row:
            if number_displayed == -1:
                return True  # Okay I don't want to deal with collision cases here
            elif number_displayed != 0:
                list_of_alive_dodgems_shown.append(number_displayed)

    assert len(list_of_alive_dodgems_shown) == len(
        set(list_of_alive_dodgems_shown)), f"The render shows duplicate dodgems.\nList of dodgems shown: {list_of_alive_dodgems_shown}\nArena:\n{arena}"

    list_of_alive_dodgems_from_classes = []

    for dodgem in dodgems_list:
        if dodgem.alive:
            list_of_alive_dodgems_from_classes.append(dodgem.dodgem_id)

    assert set(list_of_alive_dodgems_shown) == set(
        list_of_alive_dodgems_from_classes), f"There appears to be a mismatch between the alive dodgems in the render, and the alive dodgems from the classes.\nAlive dodgems in render: {list_of_alive_dodgems_shown}\nAlive dodgems from classes: {list_of_alive_dodgems_from_classes}\nArena:\n{arena}"
