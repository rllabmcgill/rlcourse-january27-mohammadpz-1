class MDP():
    def __init__(self, config):
        self.config = config
        self.width, self.height = len(self.config.grid[0]), len(self.config.grid)
        self.grid = self.config.grid
        states = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                states.append((i, j))
        self.states = states

    def getPossibleActions(self, state):
        x, y = state
        if state == 'E':
            return ()
        if self.grid[x][y] == '-' or self.grid[x][y] == 'E':
            return ('exit',)
        return self.config.allactions

    def get_immediate_reward(self, state):
        x, y = state
        if self.grid[x][y] == '-':
            return -100
        if self.grid[x][y] == 'E':
            return 0.0
        return -1.0

    def get_next_state(self, state, action):
        x, y = state
        if self.grid[x][y] == '-' or self.grid[x][y] == 'E':
            return 'E'
        index = self.config.allactions.index(action)
        if (self.is_allowed(y + self.config.dy[index], x + self.config.dx[index])):
            nextstate = (x + self.config.dx[index], y + self.config.dy[index])
        else:
            nextstate = (x, y)

        return nextstate

    def is_allowed(self, y, x):
        if y < 0 or y >= self.height:
            return False
        if x < 0 or x >= self.width:
            return False
        return True

    def apply_action_on_grid(self, state, action):
        if action is None or action == 'exit':
            return state
        index = self.config.allactions.index(action)
        x, y = state
        nextstate = (x + self.config.dx[index], y + self.config.dy[index])
        # import ipdb; ipdb.set_trace()
        if self.grid[nextstate[0]][nextstate[1]] != 'E':
            self.grid[nextstate[0]][nextstate[1]] = 'P'
        return nextstate, self.grid
