import sys
from adversarialsearchproblem import AdversarialSearchProblem


def minimax(asp):
    """
	Implement the minimax algorithm on ASPs,
	assuming that the given game is both 2-player and constant-sum

	Input: asp - an AdversarialSearchProblem
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    value = -sys.maxsize - 1
    choice = None
    # First 'max' call.
    for action in asp.get_available_actions(asp.get_start_state()):
        v = min_value(asp, asp.transition(asp.get_start_state(), action), asp.get_start_state().player_to_move())
        if v > value:
            value = v
            choice = action
    return choice

def max_value(asp, state, player):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    value = -sys.maxsize - 1
    for action in asp.get_available_actions(state):
        next_state = asp.transition(state, action)
        new_val = max(value, min_value(asp, next_state, player))
        if new_val > value:
            value = new_val
    return value

def min_value(asp, state, player):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    value = sys.maxsize
    for action in asp.get_available_actions(state):
        next_state = asp.transition(state, action)
        new_val = min(value, max_value(asp, next_state, player))
        if new_val < value:
            value = new_val
    return value

def alpha_beta(asp):
    """
	Implement the alpha-beta pruning algorithm on ASPs,
	assuming that the given game is both 2-player and constant-sum.

	Input: asp - an AdversarialSearchProblem
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    alpha = -sys.maxsize - 1
    choice = None
    # First 'max' call.
    for action in asp.get_available_actions(asp.get_start_state()):
        v = min_value_ab(asp, asp.transition(asp.get_start_state(), action),
                            asp.get_start_state().player_to_move(), alpha, sys.maxsize)
        if v > alpha:
            alpha = v
            choice = action
    return choice

def max_value_ab(asp, state, player, alpha, beta):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    for action in asp.get_available_actions(state):
        next_state = asp.transition(state, action)
        alpha = max(alpha, min_value_ab(asp, next_state, player, alpha, beta))
        if beta <= alpha:
            return alpha
    return alpha

def min_value_ab(asp, state, player, alpha, beta):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    for action in asp.get_available_actions(state):
        next_state = asp.transition(state, action)
        beta = min(beta, max_value_ab(asp, next_state, player, alpha, beta))
        if beta <= alpha:
            return beta
    return beta


def alpha_beta_cutoff(asp, cutoff_ply, eval_func):
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
    alpha = -sys.maxsize - 1
    beta = sys.maxsize
    choice = None
    # First 'max' call.
    first_state = asp.get_start_state()
    for action in list(asp.get_safe_actions(first_state.board, first_state.player_locs[first_state.ptm])):
        v = min_value_ab_cutoff(asp, asp.transition(first_state, action),
            first_state.ptm, alpha, beta, cutoff_ply - 1, eval_func)
        if v > alpha:
            alpha = v
            choice = action
    return choice

def max_value_ab_cutoff(asp, state, player, alpha, beta, cutoff_ply, eval_func):
    if cutoff_ply == 0:
        return eval_func(state)
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    for action in list(asp.get_safe_actions(state.board, state.player_locs[state.ptm])):
        next_state = asp.transition(state, action)
        alpha = max(alpha, min_value_ab_cutoff(asp, next_state, player, alpha, beta, cutoff_ply - 1, eval_func))
        if beta <= alpha:
            return alpha
    return alpha

def min_value_ab_cutoff(asp, state, player, alpha, beta, cutoff_ply, eval_func):
    if cutoff_ply == 0:
        return eval_func(state)
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    for action in list(asp.get_safe_actions(state.board, state.player_locs[state.ptm])):
        next_state = asp.transition(state, action)
        beta = min(beta, max_value_ab_cutoff(asp, next_state, player, alpha, beta, cutoff_ply - 1, eval_func))
        if beta <= alpha:
            return beta
    return beta


def general_minimax(asp):
    """
	Implement the generalization of the minimax algorithm that was
	discussed in the handout, making no assumptions about the
	number of players or reward structure of the given game.

	Input: asp - an AdversarialSearchProblem
	Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
	"""
    value = -sys.maxsize - 1
    choice = None
    # First 'max' call.
    for action in asp.get_available_actions(asp.get_start_state()):
        v = gen_min_value(asp, asp.transition(asp.get_start_state(), action), asp.get_start_state().player_to_move())
        if v > value:
            value = v
            choice = action
    return choice

def gen_max_value(asp, state, player):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    value = -sys.maxsize - 1
    for action in asp.get_available_actions(state):
        next_state = asp.transition(state, action)
        if next_state.player_to_move() == player:
            new_val = max(value, gen_max_value(asp, next_state, player))
        else:
            new_val = max(value, gen_min_value(asp, next_state, player))
        if new_val > value:
            value = new_val
    return value

def gen_min_value(asp, state, player):
    if asp.is_terminal_state(state):
        return asp.evaluate_state(state)[player]
    value = sys.maxsize
    for action in asp.get_available_actions(state):
        next_state = asp.transition(state, action)
        if next_state.player_to_move() == player:
            new_val = min(value, gen_max_value(asp, next_state, player))
        else:
            new_val = min(value, gen_min_value(asp, next_state, player))
        if new_val < value:
            value = new_val
    return value
