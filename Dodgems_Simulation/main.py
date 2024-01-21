from Arena import Arena

arena_size = 5
dodgem_policies = ["Random", "Random", "Random"]

arena = Arena(arena_size=5, n_dodgems=len(dodgem_policies), dodgem_policies=dodgem_policies, time_limit=1000)

if __name__ == "__main__":
    while not arena.terminated:
        arena.step()
