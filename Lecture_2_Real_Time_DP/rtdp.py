import numpy as np


class RTDP(object):

    def __init__(self, mdp, config):
        self.mdp = mdp
        self.config = config
        self.values = {}

    # v(s)
    def state_value_function(self, state):
        if state in self.values.keys():
            return self.values[state]
        return 0

    # q(s, a)
    def action_value_function(self, state, action):
        if action is None:
            return self.state_value_function(state)
        nextstate = self.mdp.get_next_state(state, action)
        nextstate_value = self.state_value_function(nextstate)
        reward = self.mdp.get_immediate_reward(state)
        val = reward + self.config.discount * nextstate_value
        return val

    # Only if the value gets better! Otherwise it stays the same.
    # def update_value_function_and_go_to_next_state(self, state, action):
    #     actions = self.mdp.getPossibleActions(state)
    #     best_action = None
    #     for action in actions:
    #         value_of_action = self.action_value_function(state, action)
    #         if value_of_action > self.values[state]:
    #             self.values[state] = value_of_action
    #             best_action = action
    #     return self.mdp.get_next_state(state, best_action)

    # Credit to https://github.com/snmnmin12/Mdp-solver
    # RTDP here chooses the best path and updates the values
    def apply_RTDP(self, start_state):
        for iter in range(self.config.iteration):
            state = start_state
            while (state != 'E'):
                actions = self.mdp.getPossibleActions(state)
                qvalue = -np.inf
                best_action = None
                for action in actions:
                    value_of_action = self.action_value_function(state, action)
                    if value_of_action > qvalue:
                        qvalue = value_of_action
                        best_action = action
                self.values[state] = qvalue
                state = self.mdp.get_next_state(state, best_action)

    def next_best_action(self, state):
        self.apply_RTDP(state)
        qvalue = -np.inf
        best_action = None
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            value_of_action = self.action_value_function(state, action)
            if value_of_action > qvalue:
                qvalue = value_of_action
                best_action = action
        return best_action
