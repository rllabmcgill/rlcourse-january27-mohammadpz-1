from MDP import MDP
from rtdp import RTDP
import config
from utils import print_grid, get_start_and_end_states
import time

mdp = MDP(config)
start, end = get_start_and_end_states(config.grid)
config.start = start
config.end = end
state = start
states = [state]
a = RTDP(mdp, config)
action = None
while action != 'exit':
    action = a.next_best_action(state)
    state, grid = mdp.apply_action_on_grid(state, action)
    if type(grid) != int:
        print_grid(grid)
    # time.sleep(0.1)
    states.append(state)
