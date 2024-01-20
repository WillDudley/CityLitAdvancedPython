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
            self.add_dodgem(i+1)


    def add_dodgem(self, dodgem_id):
        """
        Create a new dodgem, add it to the list of dodgems, and place it in a random square in the arena
        :return:
        """

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

        self.dodgems.append(Dodgem(hit_points=1,
                                   speed=1,
                                   pursuit_strategy=None,
                                   current_location=np.array([x_coordinate, y_coordinate]),
                                   dodgem_id=dodgem_id))

        self.arena[x_coordinate, y_coordinate] = self.dodgems[-1].dodgem_id  # Set the randomly chosen arena coordinate to the ID of the newly created dodgem

    def _plot(self):
        pass

    def _render(self):
        print(self.arena)

    def step(self):
        # Move dodgems if they are alive
        for dodgem in self.dodgems:
            if dodgem.alive:
                self.arena[dodgem.current_location[0], dodgem.current_location[1]] = 0

                #print(f"current location for dodgem {dodgem.dodgem_id}: {dodgem.current_location[0]}, {dodgem.current_location[1]}")

                dodgem.step()

                #print(f"updated location for dodgem {dodgem.dodgem_id}: {dodgem.current_location[0]}, {dodgem.current_location[1]}")


                # account for collision with wall
                for i in [0, 1]:
                    if dodgem.current_location[i] >= self.arena_size:
                        dodgem.current_location[i] -= 1
                    elif dodgem.current_location[i] < 0:
                        dodgem.current_location[i] += 1

                #print(f"updated location for dodgem {dodgem.dodgem_id} after collision check: {dodgem.current_location[0]}, {dodgem.current_location[1]}")

                #print(self.arena)
                self.arena[dodgem.current_location[0], dodgem.current_location[1]] = dodgem.dodgem_id
            #print(self.arena)


        # Assess for collisions
        coordinate_list=[tuple(dodgem.current_location) for dodgem in self.dodgems]

        for dup in sorted(list_duplicates(coordinate_list)):  # https://stackoverflow.com/a/5419576
            # there is a bug here where dead dodgems persist in dup, meaning that any dodgem that collides with a square where another dodgem died is destroyed
            for i in dup[1]:
                if self.dodgems[i].alive:
                    self.dodgems[i].alive = False
                    self.arena[self.dodgems[i].current_location[0], self.dodgems[i].current_location[1]] = 0

            print(dup)
        self._render()
        # Plot

        self.time_step += 1
        if self.time_step >= self.time_limit:
            self.terminated = True


def list_duplicates(seq): # https://stackoverflow.com/a/5419576
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items()
                            if len(locs)>1)