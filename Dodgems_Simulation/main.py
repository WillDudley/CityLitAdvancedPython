from Arena import Arena

arena_size = 3
dodgem_policies = ["SE", "SE", "SE"]

arena = Arena(arena_size=arena_size, n_dodgems=len(dodgem_policies), dodgem_policies=dodgem_policies, time_limit=1000)

if __name__ == "__main__":
    while not arena.terminated:
        arena.step()
