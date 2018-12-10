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


class CloudBot:
    """ Write your student bot here"""
    def __init__(self):
        self.prediction_depth = 4
        self.hunt_down_distance = 8
        self.whoami = None
        self.initial_state = True
        self.attack_weight = 1

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
        self.whoami = ptm
        other_loc = locs[abs(ptm-1)]
        possibilities = list(TronProblem.get_armor_safe_actions(state, loc))

        # Defeat.
        if not possibilities:
            print("decided there were no possibilities available")
            return "U"

        if self.initial_state:
            # print("unreachable search start")
            if not self.reachable(asp):
                self.initial_state = False
            # print("unreachable search end")
        if self.initial_state:
            current_distance = self.estimated_distance(loc, other_loc)
            # print("cur dist:", current_distance)
            if (current_distance > self.hunt_down_distance):
                # print("hunt down pt. 1")
                decision = self.hunt_down(possibilities, loc, other_loc)
                print("hunt down decision:", decision)
                if  decision == None:
                    self.initial_state = False
                else:
                    print("chose1:", decision)
                    return decision
            else:
                self.initial_state = False
        print("armor safe actions 1:", possibilities)
        print("armor safe actions:", asp.get_armor_safe_actions(state, loc))
        
        decision = a_search.alpha_beta_cutoff_fabrice(asp, self.prediction_depth, self.eval_func)
        # decision = a_search.alpha_beta_cutoff(asp, self.prediction_depth, self.eval_func)
        print("chose2:", decision)
        return decision

    def reachable(self, asp):
        return a_search.astar(asp, a_search.astar_heurisic)


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
        self.whoami = None
        self.initial_state = True

    def estimated_distance(self, loc1, loc2):
        return (abs(loc1[0] - loc2[0])) + (abs(loc1[1] - loc2[1]))

    def hunt_down(self, possibilities, loc1, loc2):
        horiz_diff = loc1[1] - loc2[1]
        vertical_diff = loc1[0] - loc2[0]
        # print("vert:", abs(vertical_diff))
        # print("horiz:", abas(horiz_diff))
        if abs(vertical_diff) > abs(horiz_diff):
            if vertical_diff > 0:
                if "U" in possibilities:
                    return "U"
            else:
                if "D" in possibilities:
                    return "D"
        else:
            if horiz_diff < 0:
                if "R" in possibilities:
                    return "R"
            else:
                if "L" in possibilities:
                    return "L"
        return None

    def eval_func(self, state):
        # print("player index: ", state.ptm)
        # very bad if we die
        locPlayer = state.player_locs[self.whoami]
        if locPlayer == None:
            return -9999999
        locOpp = state.player_locs[abs(self.whoami - 1)]
        if locOpp == None:
            return 9999999
        board = state.board
        # check if the space is divided
        # if self.space_divided(self.whoami, state):
        playerSpaces = self.open_spaces(locPlayer, state)
        #print("player spaces: ", playerSpaces)
        # if self.space_divided(self.whoami, state):
        oppSpaces = self.open_spaces(locOpp, state)
        # print("opp spaces: ", oppSpaces)
        return playerSpaces - (self.attack_weight*oppSpaces)

    def open_spaces(self, loc, state):
        # doesn't take into account that going one way shuts off all the other ways...
        # like some moves are mutually exclusive
        visited = set()
        q = queue.Queue()
        cloud_sizes = {}
        cloud = {}
        cloud_sizes[1] = 0
        # print("loc:", loc)
        for move in list(TronProblem.get_safe_actions(state.board, loc)):
            next_loc = TronProblem.move(loc, move)
            #print("next loc:", next_loc)
            my_cloud = len(cloud) + 1
            #print("my cloud", my_cloud)
            cloud[next_loc] = my_cloud
            cloud_sizes[my_cloud] = 1
            q.put(next_loc)
            visited.add(next_loc)
        while not q.empty():
            new_loc = q.get()
            # print("new loc:", new_loc)
            for move in list(TronProblem.get_safe_actions(state.board, new_loc)):
                next_loc = TronProblem.move(new_loc, move)
                if next_loc in cloud:
                    new_cloud = cloud[next_loc]
                    old_cloud = cloud[new_loc]
                    if not new_cloud == old_cloud:
                        # combine pointers to other clouds
                        #print("clouds !=:", cloud_sizes, new_cloud, old_cloud)
                        if cloud_sizes[new_cloud] < 0 and cloud_sizes[old_cloud] < 0:
                            if not new_cloud == old_cloud:
                                cloud_sizes[max(old_cloud, new_cloud)] = cloud_sizes[min(old_cloud, new_cloud)]
                        # get the base "pointer"
                        while cloud_sizes[new_cloud] < 0:
                            new_cloud = abs(cloud_sizes[new_cloud])
                        while cloud_sizes[old_cloud] < 0:
                            old_cloud = abs(cloud_sizes[old_cloud])
                        # if they aren't point to the same thing, then adjust them
                        if not new_cloud == old_cloud:
                            cloud_sizes[min(old_cloud, new_cloud)] += cloud_sizes[max(old_cloud, new_cloud)]
                            cloud_sizes[max(old_cloud, new_cloud)] = -1 * min(old_cloud, new_cloud)
                else:
                    my_cloud = cloud[new_loc]
                if next_loc not in visited:
                    cloud[next_loc] = my_cloud
                    # print("cloudsizes:", cloud_sizes, my_cloud)
                    while cloud_sizes[my_cloud] < 0:
                        my_cloud = abs(cloud_sizes[my_cloud])
                    cloud_sizes[my_cloud] += 1
                    # print("clouds new:", cloud_sizes)
                    q.put(next_loc)
                    visited.add(next_loc)

        #print("cloud sizes:", cloud_sizes)
        largest_cloud_sz = 0
        for cloud, size in cloud_sizes.items():
            if size > largest_cloud_sz:
                largest_cloud_sz = size
        num_spaces = largest_cloud_sz
        return num_spaces


class AlphaBetaBot:
    """ Write your student bot here"""
    def __init__(self):
        self.prediction_depth = 4
        self.prediction_depth_separated = 4
        self.hunt_down_distance = 5
        self.reachable_opp = True
        self.whoami = None
        self.initial_state = True

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
        self.whoami = ptm
        other_loc = locs[abs(ptm-1)]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        self.reachable_opp = True

        # Defeat.
        if not possibilities:
            return "U"

        # # have different path finding if opponent is unreachable:
        # print("1")
        # if not self.reachable_opp:
        #     print("using bfs")
        #     decision = a_search.maximize_white_space(asp, self.prediction_depth_separated, self.eval_func())
        #     self.reachable_opp = False
        #     return decision
        print("2")
        if not self.reachable(asp):
            print("using bfs")
            decision = a_search.maximize_white_space(asp, self.prediction_depth_separated, self.eval_func())
            self.reachable_opp = False
            return decision
        else: #opponent is reachable
            print("opponent reachable")
            if self.initial_state:
                print("init state")
                current_distance = self.estimated_distance(loc, other_loc)
                print("cur dist:", current_distance)
                if (current_distance > self.hunt_down_distance):
                    print("hunt down pt. 1")
                    decision = self.hunt_down(possibilities, loc, other_loc)
                    if not decision == None:
                        print("hunt down pt. 2")
                        return decision
                else:
                    self.initial_state = False
        print("ab")
        decision = a_search.alpha_beta_cutoff(asp, self.prediction_depth, self.eval_func)
        # print("CURRENT STATE")
        # print(self.eval_func(state))
        return decision

    def reachable(self, asp):
        return a_search.astar(asp, a_search.astar_heurisic)
        # return not a_search.bfs(asp)


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
        self.reachable_opp = True

    def estimated_distance(self, loc1, loc2):
        return (abs(loc1[0] - loc2[0])) + (abs(loc1[1] - loc2[1]))

    def hunt_down(self, possibilities, loc1, loc2):
        horiz_diff = loc1[1] - loc2[1]
        vertical_diff = loc1[0] - loc2[0]
        print("vert:", vertical_diff)
        print("horiz:", horiz_diff)
        if abs(vertical_diff) > abs(horiz_diff):
            if vertical_diff > 0:
                if "U" in possibilities:
                    return "U"
            else:
                if "D" in possibilities:
                    return "D"
        else:
            if horiz_diff < 0:
                if "R" in possibilities:
                    return "R"
            else:
                if "L" in possibilities:
                    return "L"
        return None

    def eval_func(self, state):
        # print("player index: ", state.ptm)
        # very bad if we die
        locPlayer = state.player_locs[self.whoami]
        if locPlayer == None:
            return -9999999
        locOpp = state.player_locs[abs(self.whoami - 1)]
        if locOpp == None:
            return 9999999
        board = state.board
        # check if the space is divided
        # if self.space_divided(self.whoami, state):
        playerSpaces = self.open_spaces(locPlayer, state)
        # print("player spaces: ", playerSpaces)
        # if self.space_divided(self.whoami, state):
        oppSpaces = self.open_spaces(locOpp, state)
        # print("opp spaces: ", oppSpaces)
        return playerSpaces - oppSpaces

    def space_divided(self, player, state):
        next_moves = [TronProblem.move(state.player_locs[player], move) for move in list(TronProblem.get_safe_actions(state.board, loc))]
        for move1 in next_moves:
            for move2 in next_moves:
                if a_search.astar(asp, a_search.astar_heurisic):
                    pass
        pass

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
