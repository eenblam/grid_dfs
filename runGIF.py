from grid_dfs.simulator import GameInstance

if __name__ == '__main__':
    m = 4
    n = 6
    M = [[None, None, None, 1, None, 1],
        [None, None, 1, None, 1, 1],
        [None, None, None, 1, None, None],
        [None, None, None, None, None, None]]

    game = GameInstance(m, n, M)
    #game.random_start()
    #game.show_simulation(pause=True)
    game.gif('sim.gif')
