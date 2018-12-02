#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import adversarialsearch_tron as a_search
import random, math, queue

# Throughout this file, ASP means adversarial search problem.

class StudentBot:
    """ Write your student bot here"""
    def __init__(self):
        self.prediction_depth = 5
        self.hunt_down_distance = 5
        self.initial_state = True
        self.whoami = None

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

        other_loc = locs[abs(ptm-1)]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        # Defeat.
        if not possibilities:
            return "U"

        # # have different path finding if opponent is unreachable:
        # if self.unreachable(loc, other_loc, state):
        #     decision = a_search.maximize_white_space(asp)
        #
        # # choose next move in initial state
        # if self.initial_state:
        #     print("WE ARE IN INITIAL STATE!!!!!", self.estimated_distance(loc, other_loc))
        # if (self.estimated_distance(loc, other_loc) < self.hunt_down_distance) and self.initial_state:
        #     print("WE ARE IN INITIAL STATE!!!!! pt. 2: ", self.estimated_distance(loc, other_loc))
        #     decision = self.hunt_down(loc, other_loc)
        # else:
        #     self.initial_state = False

        # default: Choosing the next action with ab-pruning minimax.
        self.whoami = ptm
        decision = a_search.alpha_beta_cutoff(asp, self.prediction_depth, self.eval_func)
        # print("CURRENT STATE")
        # print(self.eval_func(state))
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


    # def unreachable(self, loc1, loc2, state):
    #     return False
    #
    #
    # def estimated_distance(self, loc1, loc2):
    #     return (abs(loc1[0] - loc2[0])) + (abs(loc1[1] - loc2[1]))
    #
    # def hunt_down(self, loc1, loc2):
    #     vertical_diff = loc1[1] - loc2[1]
    #     horiz_diff = loc1[0] - loc2[0]
    #     if vertical_diff > horiz_diff:
    #         if vertical_diff > 0:
    #             return "U"
    #         else:
    #             return "D"
    #     else:
    #         if horiz_diff > 0:
    #             return "R"
    #         else:
    #             return "L"


    def eval_func(self, state):
        # print("player index: ", state.ptm)
        locPlayer = state.player_locs[self.whoami]
        locOpp = state.player_locs[abs(self.whoami - 1)]
        board = state.board
        playerSpaces = self.open_spaces(locPlayer, state)
        # print("player spaces: ", playerSpaces)
        oppSpaces = self.open_spaces(locOpp, state)
        # print("opp spaces: ", oppSpaces)
        return playerSpaces - oppSpaces

    def open_spaces(self, loc, state):
        # doesn't take into account that going one way shuts off all the other ways...
        # like some moves are mutually exclusive
        visited = set()
        q = queue.Queue()
        num_spaces = 0
        # print("loc:", loc)
        for move in list(TronProblem.get_safe_actions(state.board, loc)):
            next_loc = TronProblem.move(loc, move)
            # print("next loc:", next_loc)
            q.put(next_loc)
            visited.add(next_loc)
            num_spaces += 1
        while not q.empty():
            new_loc = q.get()
            # print("new loc:", new_loc)
            for move in list(TronProblem.get_safe_actions(state.board, new_loc)):
                next_loc = TronProblem.move(new_loc, move)
                if (not next_loc in visited):
                    q.put(next_loc)
                    visited.add(next_loc)
                    num_spaces += 1
        return num_spaces


class AlphaBetaBot:
    """ Write your student bot here"""
    def __init__(self):
        self.prediction_depth = 5
        self.hunt_down_distance = 5
        self.initial_state = True
        self.whoami = None

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

        other_loc = locs[abs(ptm-1)]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        # Defeat.
        if not possibilities:
            return "U"

        # # have different path finding if opponent is unreachable:
        # if self.unreachable(loc, other_loc, state):
        #     decision = a_search.maximize_white_space(asp)
        #
        # # choose next move in initial state
        # if self.initial_state:
        #     print("WE ARE IN INITIAL STATE!!!!!", self.estimated_distance(loc, other_loc))
        # if (self.estimated_distance(loc, other_loc) < self.hunt_down_distance) and self.initial_state:
        #     print("WE ARE IN INITIAL STATE!!!!! pt. 2: ", self.estimated_distance(loc, other_loc))
        #     decision = self.hunt_down(loc, other_loc)
        # else:
        #     self.initial_state = False

        # default: Choosing the next action with ab-pruning minimax.
        self.whoami = ptm
        decision = a_search.alpha_beta_cutoff(asp, self.prediction_depth, self.eval_func)
        # print("CURRENT STATE")
        # print(self.eval_func(state))
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


    # def unreachable(self, loc1, loc2, state):
    #     return False
    #
    #
    # def estimated_distance(self, loc1, loc2):
    #     return (abs(loc1[0] - loc2[0])) + (abs(loc1[1] - loc2[1]))
    #
    # def hunt_down(self, loc1, loc2):
    #     vertical_diff = loc1[1] - loc2[1]
    #     horiz_diff = loc1[0] - loc2[0]
    #     if vertical_diff > horiz_diff:
    #         if vertical_diff > 0:
    #             return "U"
    #         else:
    #             return "D"
    #     else:
    #         if horiz_diff > 0:
    #             return "R"
    #         else:
    #             return "L"


    def eval_func(self, state):
        # print("player index: ", state.ptm)
        locPlayer = state.player_locs[self.whoami]
        locOpp = state.player_locs[abs(self.whoami - 1)]
        board = state.board
        playerSpaces = self.open_spaces(locPlayer, state)
        # print("player spaces: ", playerSpaces)
        oppSpaces = self.open_spaces(locOpp, state)
        # print("opp spaces: ", oppSpaces)
        return playerSpaces - oppSpaces

    def open_spaces(self, loc, state):
        # doesn't take into account that going one way shuts off all the other ways...
        # like some moves are mutually exclusive
        visited = set()
        q = queue.Queue()
        num_spaces = 0
        # print("loc:", loc)
        for move in list(TronProblem.get_safe_actions(state.board, loc)):
            next_loc = TronProblem.move(loc, move)
            # print("next loc:", next_loc)
            q.put(next_loc)
            visited.add(next_loc)
            num_spaces += 1
        while not q.empty():
            new_loc = q.get()
            # print("new loc:", new_loc)
            for move in list(TronProblem.get_safe_actions(state.board, new_loc)):
                next_loc = TronProblem.move(new_loc, move)
                if (not next_loc in visited):
                    q.put(next_loc)
                    visited.add(next_loc)
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
