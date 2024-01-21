from Arena import Arena

arena_size = 1000
dodgem_policies = ["Random", "Random", "Pursuit", "Escape"]
dodgem_hitpoints = [4, 2, 4, 4]
dodgem_speeds = [50, 50, 50, 50]

assert len(dodgem_policies) == len(dodgem_hitpoints) == len(dodgem_speeds), "There has to be the same number of elements in `dodgem_policies`, `dodgem_hitpoints`, and `dodgem_speeds`!"

arena = Arena(arena_size=arena_size,
              n_dodgems=len(dodgem_policies),
              dodgem_policies=dodgem_policies,
              dodgem_speeds=dodgem_speeds,
              dodgem_hitpoints=dodgem_hitpoints,
              time_limit=1000)

if __name__ == "__main__":
    while not arena.terminated:
        arena.step()
