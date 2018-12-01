#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import adversarialsearch_tron as a_search
import random, math

# Throughout this file, ASP means adversarial search problem.

class StudentBot:
    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            """
            The way WallBot decides on next moves is if the length of the safe
            actions is less than 3 (meaning it will do dumb things sometimes
            like run into walls where safe_actions == 0).
            """
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision


class AlphaBetaBot:
    """ Write your student bot here"""
    def __init__(self):
        self.prediction_depth = 5

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))

        # Defeat.
        if not possibilities:
            return "U"
        # Choosing the next action with ab-pruning minimax.
        decision = a_search.alpha_beta_cutoff(asp, self.prediction_depth, self.eval_func)

        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision

    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def eval_func(self, state):
        locPlayer = state.player_locs[state.ptm]
        locOpp = state.player_locs[math.abs(state.ptm - 1)]
        playerSpaces = open_spaces(locPlayer, state)
        oppSpaces = open_spaces(oppPlayer, state)
        return playerSpaces - oppSpaces


    def open_spaces(self, loc, state):
        visited = set()
        q = Queue()
        num_spaces = 0

        for move in list(TronProblem.get_safe_actions(state.board, loc)):
            next_loc = TronProblem.move(loc, move)
            q.put(next_loc)
            num_spaces += 1
        while q is not empty:
            new_loc = q.get()
            visited.add(new_loc)
            for move in list(TronProblem.get_safe_actions(state.board, new_loc)):
                next_loc = TronProblem.move(loc, move)
                if not next_loc in visited:
                    q.put(next_loc)
                    num_spaces += 1
        return num_spaces


class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            """
            The way WallBot decides on next moves is if the length of the safe
            actions is less than 3 (meaning it will do dumb things sometimes
            like run into walls where safe_actions == 0).
            """
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
