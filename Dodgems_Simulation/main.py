from Arena import Arena

arena = Arena(arena_size=5, n_dodgems=5, time_limit=1000)


if __name__ == "__main__":
    while not arena.terminated:
        arena.step()
