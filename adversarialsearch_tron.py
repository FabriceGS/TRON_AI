import sys
from adversarialsearchproblem import AdversarialSearchProblem
from queue import Queue, LifoQueue, PriorityQueue

def alpha_beta_cutoff_fabrice(asp, cutoff_ply, eval_func):
    """
	This function should:
	- search through the asp using alpha-beta pruning
	- cut off the search after cutoff_ply moves have been made.
	Inputs:
		asp - an AdversarialSearchProblem
		cutoff_ply- an Integer that determines when to cutoff the search
			and use eval_func.
			For example, when cutoff_ply = 1, use eval_func to evaluate
			states that result from your first move. When cutoff_ply = 2, use
			eval_func to evaluate states that result from your opponent's
			first move. When cutoff_ply = 3 use eval_func to evaluate the
			states that result from your second move.
			You may assume that cutoff_ply > 0.
		eval_func - a function that takes in a GameState and outputs
			a real number indicating how good that state is for the
			player who is using alpha_beta_cutoff to choose their action.
			You do not need to implement this function, as it should be provided by
			whomever is calling alpha_beta_cutoff, however you are welcome to write
			evaluation functions to test your implemention
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    def abCutHelper(curState, alpha, beta, maximizingPlayer, depth):
        if(depth == 0):
            return eval_func(curState)
        if (asp.is_terminal_state(curState)):
            return eval_func(curState)
        elif(curState.ptm == maximizingPlayer):
            # if armor
            # get extra actions
            #

            availActions = list(asp.get_armor_safe_actions(curState, curState.player_locs[curState.ptm]))
            for action in availActions:
                nextState = asp.transition(curState, action)
                newAlpha = abCutHelper(nextState, alpha, beta, maximizingPlayer, depth-1)
                alpha = max(alpha, newAlpha)
                if beta <= alpha:
                    return alpha
            return alpha
        else:
            availActions = list(asp.get_armor_safe_actions(curState, curState.player_locs[curState.ptm]))
            for action in availActions:
                nextState = asp.transition(curState, action)
                newBeta = abCutHelper(nextState,alpha,beta, maximizingPlayer, depth-1)
                beta = min(beta, newBeta)
                if beta <= alpha:
                    return beta
            return beta
    bestAction = "U"
    curState = asp.get_start_state()
    maximizingPlayer = asp.get_start_state().ptm
    alpha = -(sys.maxsize-1)
    beta = sys.maxsize

    if (asp.is_terminal_state(curState)):
        return "IDK"
    elif(curState.player_to_move() == maximizingPlayer):
        availActions = list(asp.get_armor_safe_actions(curState, curState.player_locs[curState.ptm]))
        for action in availActions:
            print("evaluated action: ", action)
            nextState = asp.transition(curState, action)
            newAlpha = abCutHelper(nextState, alpha, beta, maximizingPlayer, cutoff_ply -1)
            print("min value: ", newAlpha)
            if alpha < newAlpha:
                bestAction = action
                alpha = newAlpha
            if beta <= alpha:
                print("ab action:", action)
                return action
        return bestAction
    else:
        availActions = list(asp.get_armor_safe_actions(curState, curState.player_locs[curState.ptm]))
        for action in availActions:
            nextState = asp.transition(curState, action)
            newBeta = abCutHelper(nextState,alpha,beta, maximizingPlayer, cutoff_ply -1)
            if beta > newBeta:
                bestAction = action
                beta = newBeta
            if beta <= alpha:
                print("ab action:", action)
                return action
        print("ab action:", bestAction)
        return bestAction

def alpha_beta_cutoff(asp, cutoff_ply, eval_func):
    alpha = -sys.maxsize - 1
    beta = sys.maxsize
    choice = None
    # First 'max' call.
    first_state = asp.get_start_state()
    for action in list(asp.get_armor_safe_actions(first_state, first_state.player_locs[first_state.ptm])):
        # print("evaluated action: ", action)
        v = min_value_ab_cutoff(asp, asp.transition(first_state, action),
            first_state.ptm, alpha, beta, cutoff_ply - 1, eval_func)
        # print("min value: ", v)
        if v > alpha:
            alpha = v
            choice = action
        # if beta <= alpha:
        #     print("best ab action: ", )
        #     return action
    # print("alpha: ", alpha)
    # print("choice: ", choice)
    return choice

def max_value_ab_cutoff(asp, state, player, alpha, beta, cutoff_ply, eval_func):
    if cutoff_ply == 0:
        # print("this should be player 1:", state.ptm)
        return eval_func(state)
    if asp.is_terminal_state(state):
        # print("terminal state")
        return eval_func(state)
    for action in list(asp.get_armor_safe_actions(state, state.player_locs[state.ptm])):
        next_state = asp.transition(state, action)
        alpha = max(alpha, min_value_ab_cutoff(asp, next_state, player, alpha, beta, cutoff_ply - 1, eval_func))
        if beta <= alpha:
            return alpha
    return alpha

def min_value_ab_cutoff(asp, state, player, alpha, beta, cutoff_ply, eval_func):
    if cutoff_ply == 0:
        # print("this should be player 1:", state.ptm)
        return eval_func(state)
    if asp.is_terminal_state(state):
        # print("terminal state")
        return eval_func(state)
    for action in list(asp.get_armor_safe_actions(state, state.player_locs[state.ptm])):
        next_state = asp.transition(state, action)
        beta = min(beta, max_value_ab_cutoff(asp, next_state, player, alpha, beta, cutoff_ply - 1, eval_func))
        if beta <= alpha:
            return beta
    return beta


def astar_heurisic(state):
    locs = state.player_locs
    board = state.board
    ptm = state.ptm
    loc = locs[ptm]
    other_loc = locs[abs(ptm-1)]
    horiz = abs(loc[0] - other_loc[0])
    verti = abs(loc[1] - other_loc[1])
    total_distance = (horiz + verti)
    return total_distance


def astar(problem, heur):
    """
    Implement A* search.

    The given heuristic function will take in a state of the search problem
    and produce a real number

    Your implementation should be able to work with any heuristic, heur
    that is for the given search problem (but, of course, without a
    guarantee of optimality if heur is not admissible).

    Input:
        problem - the problem on which the search is conducted, a SearchProblem

    Output: a list of states representing the path of the solution

    """
    frontier = PriorityQueue()
    frontier.put((heur(problem.get_start_state()), problem.get_start_state()))
    parent = {}
    parent[problem.get_start_state()] = None
    gCost = {}
    gCost[problem.get_start_state()] = 0
    ignore = {}
    visited = set()

    while not frontier.empty() and frontier.qsize() < 500:
        current = frontier.get()[1]
        visited.add(current)
        # print("qsize: ", frontier.qsize())

        if(is_goal_state(current)):
            return True

        newGCost = gCost[current] + 1

        successors = [problem.transition(current, action) for action in list(problem.get_safe_actions(current.board, current.player_locs[current.ptm]))]
        for neighbor in successors:
            if (neighbor not in gCost and neighbor not in parent and neighbor not in visited) or (gCost[neighbor] > newGCost):
                #what do we do if the neighbor is already in the frontier
                # if neighbor not in frontier:

                # visited.add(neighbor)
                gCost[neighbor] = newGCost
                #print("cost:", (gCost[neighbor]+ heur(neighbor)))
                frontier.put((gCost[neighbor]+ heur(neighbor), neighbor))
                parent[neighbor] = current

    return False

def bfs(asp):
    frontier = Queue()
    prev_state_dict = dict()
    visited_set = set()
    start_state = asp.get_start_state()

    frontier.put(start_state)
    prev_state_dict[start_state] = None
    visited_set.add(start_state)

    while not frontier.empty():
        curr_state = frontier.get()
        # Checking if this state is the goal state.
        if is_goal_state(curr_state):
            return True

        next_states = [asp.transition(start_state, a) for a in list(asp.get_safe_actions(start_state.board, start_state.player_locs[start_state.ptm]))]

        for succ in next_states:
            if succ not in visited_set:
                frontier.put(succ)
                visited_set.add(succ)
                prev_state_dict[succ] = curr_state

    return False


def is_goal_state(state):
    locs = state.player_locs
    board = state.board
    ptm = state.ptm
    loc = locs[ptm]
    other_loc = locs[abs(ptm-1)]
    total_distance = abs(abs(loc[0] - other_loc[0]) + abs(loc[1] - other_loc[1]))
    if total_distance == 1:
        return True
    return False

def construct_path(final_state, prev_state_dict):
    solution = [final_state]
    curr_state = final_state
    while (prev_state_dict[curr_state] != None):
        prev_state = prev_state_dict[curr_state]
        solution.append(prev_state)
        curr_state = prev_state
    solution.reverse()
    return solution
