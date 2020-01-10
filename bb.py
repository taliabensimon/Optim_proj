from heapq import *
from tree import Tree, LPResult
from node import Node
import numpy as np


class MaxHeap(object):

    def __init__(self):
        self.priority_queue = []

    def add(self,data):
        #for i in data:
        item = (-data.val['fun'], data)
        heappush(self.priority_queue, item)

    def get_item(self):
        if len(self.priority_queue) == 0:
            return None
        return heappop(self.priority_queue)[1]

    def is_empty(self):
        if len(self.priority_queue) == 0:
            return Tree
        return False


class BranchAndBound(Tree):
    def __init__(self,problem):
        super(BranchAndBound, self).__init__(problem)
        self.priority_queue = MaxHeap()
        self.jump_indicator = {}
        self.node_searched = []

    def is_valid_solution(x):
        #check if the solution contins only intergers
        return all(np.equal(np.mod(x, 1), 0)) #not False in np.eq...

    def bbsolve(self):
        self.priority_queue.add(self.root)
        temp = [i if i is not None else 0 for i in self.root.var_val.copy()]
        jump = "".join(map(str, temp))
        while not self.priority_queue.is_empty():
            temp_best_node = self.priority_queue.get_item()
            self.node_searched.append(temp_best_node.var_val)
            temp = [i if i is not None else 0 for i in temp_best_node.var_val.copy()]
            x = "".join(map(str, temp))
            jump = int(x, 2) ^ int(jump, 2)
            #jump = abs(temp_best_node.level- jump)
            self.jump_indicator[jump] = self.jump_indicator.get(jump, 0) + 1
            temp = [i if i is not None else 0 for i in temp_best_node.var_val.copy()]
            x = "".join(map(str, temp))
            jump = x
            #jump = temp_best_node.level

            if not temp_best_node.not_valid:
                if temp_best_node.is_final:  # if a valid solution then this is the best
                    return temp_best_node.val, temp_best_node.var_val, self.jump_indicator, self.node_searched
                else:  # otherwise, we're unsure if this branch holds promise. Maybe it can't actually achieve this lower bound. So branch into it
                    new_nodes = self.get_children(temp_best_node)
                    for new_node in new_nodes:
                        if new_node.is_final:
                            self.priority_queue.add(new_node)
                        else:
                            res = self.lp_node_value(new_node)
                            if res['success']:#res[LPResult.SUCESS]
                                new_node.val = res['fun'] #res[LPResult.FUNC_VAL]
                                if self.is_valid_solution(res['x']):#res[LPResult.VAR_COEFF]
                                    new_node.is_final = True
                                    new_node.var_val = res['x'] #res[LPResult.VAR_COEFF]
                                self.priority_queue.add(new_node)
                            # else:
                            #     new_node.val = np.Infinity
                            #     new_node.is_final = True
                            #     new_node.not_valid = True
                        # heappush(heap, (res, next(counter), new_node))  # using counter to avoid possible comparisons between nodes. It tie breaks
        # no solution for this problem
        return None, None, self.jump_indicator, self.node_searched
