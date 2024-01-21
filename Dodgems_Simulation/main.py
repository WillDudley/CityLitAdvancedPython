from Arena import Arena

arena_size = 1000
dodgem_policies = ["Pursuit", "Random", "Escape", "Escape"]
dodgem_hitpoints = [100, 5, 10, 15]
dodgem_speeds = [20, 10, 5, 5]

assert len(dodgem_policies) == len(dodgem_hitpoints) == len(dodgem_speeds), "There has to be the same number of elements in `dodgem_policies`, `dodgem_hitpoints`, and `dodgem_speeds`!"

arena = Arena(arena_size=arena_size,
              n_dodgems=len(dodgem_policies),
              dodgem_policies=dodgem_policies,
              dodgem_speeds=dodgem_speeds,
              dodgem_hitpoints=dodgem_hitpoints,
              time_limit=100_000,
              render=False)

if __name__ == "__main__":
    while not arena.terminated:
        arena.step()
