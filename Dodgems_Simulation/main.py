from Arena import Arena

arena = Arena(arena_size=5, n_dodgems=5, time_limit=1000)

while not arena.terminated:
    arena.step()

    # Current bug is remaining dodgem destroys itself