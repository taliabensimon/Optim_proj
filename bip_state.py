from copy import deepcopy
from mcts import mcts
from tree import Tree,LPResult
import numpy as np

class BinaryIntegerProgramming(Tree):
    def __init__(self, root, node):
        self.root = root
        self.curr = node

    def getPossibleActions(self):
        possible_children = []
        node_children = self.curr.get_children()#self.get_children(self.curr)
        for child in node_children:
            # child.val = self.lp_node_value(child.problem)
            self.curr.add_child(child)
            if child.val >= self.root.val:
                possible_children.append(Action(child))#TODO:KEEPTHIS
        # return node_children
        return possible_children


    def takeAction(self, action):
        new_state = BinaryIntegerProgramming(self.root, action.node)
        return new_state

    def has_valid_child(self):
        for child in self.curr.get_children():
            if child.val != None and child.val >= self.root.val:
                return True
        return False

    def isTerminal(self):
        return self.curr.is_final or len(self.curr.get_children()) == 0 or self.has_valid_child() == False

    def is_bad_terminal(self):
        return len(self.curr.get_children()) == 0

    def getReward(self):
        if len(self.curr.get_children()) > 0 and not self.has_valid_child():
            self.curr.val = -np.inf
            self.curr.not_valid = True
        res = self.lp_node_value(self.curr.problem)
        if not res[LPResult.SUCESS]:
            self.curr.val = -np.inf
            self.curr.is_valid = False
        return res[LPResult.FUNC_VAL] if res[LPResult.SUCESS] == True else -np.inf


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
        return self.__class__ == other.__class__ and self.node.val == other.node.val and self.node.heuristic_val == other.node.heuristic_val and self.node.problem == other.node.problem


    def __hash__(self):
        return hash((self.node.val, self.node.heuristic_val, self.node.get_level(),self.node.problem))