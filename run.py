from grid_dfs.simulator import GameInstance

if __name__ == '__main__':
    unit = GameInstance(1, 1, [[1]])
    assert unit.complete()
    unit.show_simulation(2)
    two_by_two = GameInstance(2, 2, [[1,1],[1,1]])
    assert two_by_two.complete()
    two_by_two.show_simulation(2)

    game = GameInstance(10, 10)
    game.random_start()
    game.show_simulation(pause=True)
