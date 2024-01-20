from Arena import Arena

arena = Arena(arena_size=5, n_dodgems=3, time_limit=4)

while not arena.terminated:
    arena.step()

    # Current bug is remaining dodgem destroys itself