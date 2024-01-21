from Arena import Arena

arena_size = 3
dodgem_policies = ["Random", "Random"]
dodgem_hitpoints = [4, 2]

assert len(dodgem_policies) == len(dodgem_hitpoints), "There has to be the same number of elements in both `dodgem_policies` and `dodgem_hitpoints`!"

arena = Arena(arena_size=arena_size,
              n_dodgems=len(dodgem_policies),
              dodgem_policies=dodgem_policies,
              dodgem_hitpoints=dodgem_hitpoints,
              time_limit=1000)

if __name__ == "__main__":
    while not arena.terminated:
        arena.step()
