from copy import deepcopy
from monte_carlo import mcts
from tree import Tree,LPResult
import numpy as np

class BinaryIntegerProgramming(Tree):
    def __init__(self, root, node = None):
        self.root = root
        self.curr = node if node is not None else self.root
        if node is None: # Set root
            self.curr.h_val = self.lp_node_value(self.curr.problem)['fun']

        if node is not None and not self.curr.is_final:
            res, val = self.get_lp_addition(self.curr.var_val, self.curr.level, self.curr.problem)
            if res["success"] and round(val,4) >= round(self.root.h_val,4) and abs(self.root.h_val - val) < 600:
                self.curr.h_val = val
                if self.is_valid_solution(res['x']):
                    self.curr.val = val
                    self.curr.is_final = True
                    for i, v in enumerate(res['x']):
                        self.curr.var_val[i + self.curr.level] = int(v)
            else:
                self.curr.set_not_valid()
        # print(f"new eval {self.curr.val}")

    def get_possible_actions(self):
        possible_children = []
        node_children = self.curr.get_children()#self.get_children(self.curr)
        for child in node_children:
            # child.val = self.lp_node_value(child.problem)
            # self.curr.add_child(child)
            if not child.not_valid and (child.h_val is None or (round(child.h_val,4) >= round(self.root.h_val,4) and child.h_val != - np.inf)) :
                possible_children.append(Action(child))
            elif not child.not_valid and child.h_val is not None:
                print()
        # return node_children
        return possible_children

    def get_possible_solution(self):
        var_count = len(self.curr.var_val[self.curr.level:])
        var_val = np.concatenate((self.curr.var_val[:self.curr.level], np.random.randint(0,2,(var_count))))
        for i,c in enumerate(self.root.problem.constraint_coeff):
            if np.dot(var_val, c) > self.root.problem.constraint_bound[i]:
                return -np.inf
        return np.dot(var_val, self.root.problem.func_coeff)

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
            self.curr.set_not_valid()
        if self.curr.is_final:
            assert self.curr.val is not None
            return self.curr.val
        res, val = self.get_lp_addition(self.curr.var_val, self.curr.level, self.curr.problem)
        if not res["success"]:
            self.curr.set_not_valid()

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