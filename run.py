from grid_dfs.simulator import GameInstance

if __name__ == '__main__':
    unit = GameInstance(1, 1, [[1]])
    assert unit.complete()
    unit.show_simulation(2)
    two_by_two = GameInstance(2, 2, [[1,1],[1,1]])
    assert two_by_two.complete()
    two_by_two.show_simulation(2)

    m = 4
    n = 6
    M = [[None, None, None, 1, None, 1],
        [None, None, 1, None, 1, 1],
        [None, None, None, 1, None, None],
        [None, None, None, None, None, None]]

    #game = GameInstance(m, n, M)
    game = GameInstance(10, 10)
    game.random_start()
    game.show_simulation(pause=True)
    #game.gif('sim.gif')
