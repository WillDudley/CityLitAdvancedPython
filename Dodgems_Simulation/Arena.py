import numpy as np
from Dodgem import Dodgem
from collections import defaultdict


class Arena:
    def __init__(self, arena_size, n_dodgems, time_limit):
        self.arena_size = arena_size
        self.n_dodgems = n_dodgems
        self.time_limit = time_limit

        self.arena = np.zeros((arena_size, arena_size))  # Create the arena
        self.dodgems = []  # Create empty list that will hold the dodgems objects
        self.terminated = False
        self.time_step = 0

        for i in list(range(n_dodgems)):
            self.add_dodgem(i + 1, False)

        self._render()

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

        self.dodgems.append(Dodgem(hit_points=1,
                                   speed=1,
                                   pursuit_strategy=None,
                                   current_location=np.array([x_coordinate, y_coordinate]),
                                   dodgem_id=dodgem_id))

        self.arena[x_coordinate, y_coordinate] = self.dodgems[
            -1].dodgem_id  # Set the randomly chosen arena coordinate to the ID of the newly created dodgem

    def _plot(self):
        pass

    def _render(self):
        print(self.arena)

    def step(self):
        # Move dodgems if they are alive
        for dodgem in self.dodgems:
            if dodgem.alive:

                # replace old position with 0 UNLESS a new dodgem has already entered the space
                if self.arena[dodgem.current_location[0], dodgem.current_location[1]] == dodgem.dodgem_id:
                    self.arena[dodgem.current_location[0], dodgem.current_location[1]] = 0

                dodgem.step()

                # account for collision with wall
                for i in [0, 1]:
                    if dodgem.current_location[i] >= self.arena_size:
                        dodgem.current_location[i] -= 1
                    elif dodgem.current_location[i] < 0:
                        dodgem.current_location[i] += 1

                # replace new position with dodgem_id - crash logic is handled later
                self.arena[dodgem.current_location[0], dodgem.current_location[1]] = dodgem.dodgem_id

        # Assess for collisions by looking at the coordinates of all alive dodgems, checking for overlaps
        coordinate_list = [tuple(dodgem.current_location) if dodgem.alive else None for dodgem in self.dodgems]
        print([d.alive for d in self.dodgems])
        print(f"Coordinate list: {coordinate_list}")

        print(f"list of duplicates: {list_duplicates(coordinate_list)}")
        for index, collision_coord in list_duplicates(coordinate_list):  # https://stackoverflow.com/a/5419576
            # If the dodgem is where another dodgem is, replace the location by "-1" and damage it
            self.dodgems[index].decrement_hp()
            self.arena[collision_coord[0], collision_coord[1]] = -1

        test_alive_dodgems_sync_with_arena_render(self.arena, self.dodgems)

        self._render()
        # Plot

        self.time_step += 1
        if self.time_step >= self.time_limit:
            self.terminated = True


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
    return duplicates


def test_alive_dodgems_sync_with_arena_render(arena: np.array, dodgems_list: list[Dodgem]):
    # I could use itertools or zip() here but I'm not confident enough
    list_of_alive_dodgems_shown = []

    for row in arena:
        for number_displayed in row:
            if number_displayed not in [0, -1]:
                list_of_alive_dodgems_shown.append(number_displayed)

    assert len(list_of_alive_dodgems_shown) == len(
        set(list_of_alive_dodgems_shown)), f"The render shows duplicate dodgems.\nList of dodgems shown: {list_of_alive_dodgems_shown}\nArena:\n{arena}"

    list_of_alive_dodgems_from_classes = []

    for dodgem in dodgems_list:
        if dodgem.alive:
            list_of_alive_dodgems_from_classes.append(dodgem.dodgem_id)

    assert set(list_of_alive_dodgems_shown) == set(
        list_of_alive_dodgems_from_classes), f"There appears to be a mismatch between the alive dodgems in the render, and the alive dodgems from the classes.\nAlive dodgems in render: {list_of_alive_dodgems_shown}\nAlive dodgems from classes: {list_of_alive_dodgems_from_classes}\nArena:\n{arena}"
