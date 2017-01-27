# Credits to https://github.com/jlynchkun
states = {
    '01', '02', '03', '04',
    '05', '06', '07', '08',
    '09', '10', '11', '12',
    '13', '14', '15', '16'}

actions = {'up', 'down', 'left', 'right'}

allowed_transitions = {
    '01': {},  # Terminal state
    '02': {'up': '02', 'down': '06', 'left': '01', 'right': '03'},
    '03': {'up': '03', 'down': '07', 'left': '02', 'right': '04'},
    '04': {'up': '04', 'down': '08', 'left': '03', 'right': '04'},
    '05': {'up': '01', 'down': '09', 'left': '05', 'right': '06'},
    '06': {'up': '02', 'down': '10', 'left': '05', 'right': '07'},
    '07': {'up': '03', 'down': '11', 'left': '06', 'right': '08'},
    '08': {'up': '04', 'down': '12', 'left': '07', 'right': '08'},
    '09': {'up': '05', 'down': '13', 'left': '09', 'right': '10'},
    '10': {'up': '06', 'down': '14', 'left': '09', 'right': '11'},
    '11': {'up': '07', 'down': '15', 'left': '10', 'right': '12'},
    '12': {'up': '08', 'down': '16', 'left': '11', 'right': '12'},
    '13': {'up': '09', 'down': '13', 'left': '13', 'right': '14'},
    '14': {'up': '10', 'down': '14', 'left': '13', 'right': '15'},
    '15': {'up': '11', 'down': '15', 'left': '14', 'right': '16'},
    '16': {}}  # Terminal state


# these are the probabilities of each result given an action
p_a_given_a = {
    'up': {'up': 0.1, 'down': 0.8, 'left': 0.1, 'right': 0.1},
    'down': {'up': 0.0, 'down': 0.8, 'left': 0.1, 'right': 0.1},
    'left': {'up': 0.1, 'down': 0.1, 'left': 0.8, 'right': 0.0},
    'right': {'up': 0.1, 'down': 0.1, 'left': 0.0, 'right': 0.8}
}

reward = {
    '01': 0.0,
    '02': -1.0,
    '03': -1.0,
    '04': -1.0,
    '05': -1.0,
    '06': -1.0,
    '07': -1.0,
    '08': -1.0,
    '09': -1.0,
    '10': -1.0,
    '11': -1.0,
    '12': -1.0,
    '13': -1.0,
    '14': -1.0,
    '15': -1.0,
    '16': 0.0}

random_policy = {
    '11': {'right': '12'},
    '10': {'left': '09'},
    '13': {'right': '14'},
    '12': {'down': '16'},
    '15': {'up': '11'},
    '14': {'up': '10'},
    '04': {'up': '04'},
    '16': {},
    '03': {'down': '07'},
    '08': {'down': '12'},
    '09': {'right': '10'},
    '02': {'down': '06'},
    '01': {},
    '06': {'up': '02', 'down': '10'},
    '05': {'down': '09'},
    '07': {'up': '03'}}

gamma = 0.9


def next_actions_list(state, action):
    action_list = []
    for a in actions:
        p_a = p_a_given_a[action][a]
        next_state = allowed_transitions[state][a]
        action_list.append((a, p_a, next_state))
    return action_list


# U is the value function over states
def bellman(U, state, policy=None):
    if policy is None:
        policy = allowed_transitions
    if len(policy[state].keys()) == 0:
        # Terminal state
        return reward[state], None
    else:
        sum_for_action = {
            action: 0.0 for action in policy[state].keys()}
        for action in policy[state].keys():
            next_actions = next_actions_list(state, action)
            for a, p_a, next_state in next_actions:
                sum_for_action[action] += p_a * U[next_state]
        (maximizing_action, maximum_sum) = max(
            sum_for_action.items(),
            key=lambda x: x[1])
        return reward[state] + gamma * maximum_sum, maximizing_action


def policy_iteration():
    iter = 0
    policy = random_policy
    U = {state: 0.0 for state in states}
    unchanged = False
    while not unchanged:
        iter += 1
        Up = U.copy()
        for key in Up.keys():
            Up[key] = round(Up[key], 1)
        print "\n  Value Function, iter:" + str(iter)
        print "|-------|-------|-------|-------|"
        print "|   " + str(Up['01']) + " |  " + str(Up['02']) + "  |  " + str(Up['03']) + "  |  " + str(Up['04']) + "  |"
        print "|-------|-------|-------|-------|"
        print "|  " + str(Up['05']) + " |  " + str(Up['06']) + "  |  " + str(Up['07']) + "  |  " + str(Up['08']) + "  |"
        print "|-------|-------|-------|-------|"
        print "|  " + str(Up['09']) + " |  " + str(Up['10']) + "  |  " + str(Up['11']) + "  |  " + str(Up['12']) + "  |"
        print "|-------|-------|-------|-------|"
        print "|  " + str(Up['13']) + " |  " + str(Up['14']) + "  |  " + str(Up['15']) + "  |  " + str(Up['16']) + "  |"
        print "|-------|-------|-------|-------|"
        # import ipdb; ipdb.set_trace()
        U = policy_evaluation(policy, U)
        unchanged = True
        for s in states:
            U_s, maximizing_action = bellman(U, s)
            U_policy, policy_action = bellman(U, s, policy)
            if U_s > U_policy:
                end_state = allowed_transitions[s][maximizing_action]
                policy[s] = {maximizing_action: end_state}
                unchanged = False
    return U, policy


def policy_evaluation(policy, u):
    u_1 = u.copy()
    for k in range(10):
        u_0 = u_1.copy()
        for state in u_0:
            u_1[state], action = bellman(u_0, state, policy)
    return u_1

U, policy = policy_iteration()
print "\nThe Optimal Policy:"
for state in states:
    if state in policy:
        try:
            a = policy.get(state).keys()[0]
            next_state = policy.get(state).values()[0]
        except:
            a = 'NONE'
            next_state = state
        print("State " + state + " -- " + a + " --> State " + next_state)
