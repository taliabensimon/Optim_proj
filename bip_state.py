from copy import deepcopy
from monte_carlo import mcts
from tree import Tree,LPResult
import numpy as np

class BinaryIntegerProgramming(Tree):
    def __init__(self, root, node = None):
        self.root = root
        self.curr = node if node is not None else self.root
        if not self.curr.is_final:
            self.curr.h_val = self.lp_node_value(self.curr.problem)['fun']
        # print(f"new eval {self.curr.val}")

    def getPossibleActions(self):
        possible_children = []
        node_children = self.curr.get_children()#self.get_children(self.curr)
        for child in node_children:
            # child.val = self.lp_node_value(child.problem)
            # self.curr.add_child(child)
            if not child.not_valid and (child.h_val is None or child.h_val >= self.root.h_val):
                possible_children.append(Action(child))
        # return node_children
        return possible_children


    def takeAction(self, action):
        new_state = BinaryIntegerProgramming(self.root, action.node)
        return new_state

    def has_valid_child(self):
        for child in self.curr.get_children():
            if not child.not_valid:
                return True
        return False

    def get_num_explored_valid_children(self):
        count = 0
        for child in self.curr.get_children():
            if child.val != None and child.val >= self.root.val:
                count += 1
        return count

    def isTerminal(self):
        return self.curr.is_final or len(self.curr.get_children()) == 0 or self.has_valid_child() == False

    def is_bad_terminal(self):
        return len(self.curr.get_children()) == 0

    def getReward(self):
        if len(self.curr.get_children()) > 0 and not self.has_valid_child():
            self.curr.val = -np.inf
            self.curr.not_valid = True
        if self.curr.is_final:
            assert self.curr.val is not None
            return self.curr.val
        res, val = self.get_lp_addition(self.curr.var_val, self.curr.level, self.curr.problem)
        if not res["success"]:
            self.curr.val = -np.inf
            self.curr.not_valid = True
        return val if res["success"] else -np.inf


class Action():
    def __init__(self, node):
        self.node = node

    # def __str__(self):
    #     return str((self.x, self.y))
    #
    # def __repr__(self):
    #     return str(self)
    #
    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.node.val == other.node.val and self.node.h_val == other.node.h_val and self.node.problem == other.node.problem and self.node.var_val == other.node.var_val


    def __hash__(self):
        return hash((self.node.val, self.node.h_val, self.node.get_level(),self.node.problem))