from heapq import *
from tree import Tree, LPResult
from node import Node
import numpy as np
import time
from monte_carlo import LimitType


class MaxHeap(object):

    def __init__(self):
        self.priority_queue = []

    def add(self,data,num):
        item = (data.val, num, data)
        heappush(self.priority_queue, item)

    def get_item(self):
        if len(self.priority_queue) == 0:
            return None
        return heappop(self.priority_queue)[2]

    def is_empty(self):
        if len(self.priority_queue) == 0:
            return Tree
        return False


class BranchAndBound(Tree):
    def __init__(self,problem,limiType=LimitType.unbounded,limit=None):
        super(BranchAndBound, self).__init__(problem)
        if self.best_possible_val is None:
            self.root.set_not_valid()
        self.priority_queue = MaxHeap()
        self.jump_indicator = {}
        self.node_searched = []
        self.best_node_till_now = None
        self.limitType = limiType
        self.limit=limit
        if limiType != LimitType.unbounded:
            self.result = {k: [] for k in range(len(limit))}
        else:
            self.result = {-1: []}

    def is_valid_solution(self, x):
        #check if the solution contins only intergers
        return all(np.equal(np.mod(x, 1), 0)) #not False in np.eq...

    def calculate_jump(self,temp_best_node,jump_level,temp_varval2):
        min_level = min(jump_level, temp_best_node.level)
        if min_level == 0:
            level_diff = abs(jump_level - temp_best_node.level)
            self.jump_indicator[level_diff] = self.jump_indicator.get(level_diff, 0) + 1

        else:
            temp_varval = temp_best_node.var_val.copy()[:min_level]
            temp_varval2 = temp_varval2[:min_level]
            tyt = "".join(map(str, temp_varval))
            yt = "".join(map(str, temp_varval2))
            level_diff = abs(jump_level - temp_best_node.level)
            jump1 = bin(int(tyt, 2) ^ int(yt, 2))[2:].zfill(len(tyt)).find('1')
            if jump1 == -1:
                jump1 = 0
            else:
                jump1 = min_level -1 - jump1  # if brathers =2 and father and sun = 1 then remove -1
                jump1 = 2 ** jump1
            if jump1 == 0 and level_diff == 1: # father to sun = 0
                test_temp = 0
            else:
                test_temp = jump1 + level_diff
            self.jump_indicator[test_temp] = self.jump_indicator.get(test_temp, 0) + 1

    def bbsolve(self):
        limit_iter = 0
        if self.limitType is not None and self.limitType == LimitType.time:
            timeLimit = time.time() + self.limit[limit_iter] / 1000
        num = 0
        self.priority_queue.add(self.root,num)
        num += 1
        temp = [i if i is not None else 0 for i in self.root.var_val.copy()]
        jump_level = 0
        temp_varval2 = self.root.var_val.copy()
        while not self.priority_queue.is_empty():
            if self.limitType is not LimitType.unbounded:
                if self.limitType == LimitType.time:

                    while time.time() > timeLimit and limit_iter < len(self.limit):
                        if self.best_node_till_now is None:
                            self.result[limit_iter].extend([None, None, self.jump_indicator, self.node_searched])
                        else:
                            self.result[limit_iter].extend([self.best_node_till_now.val, self.best_node_till_now.var_val, self.jump_indicator, self.node_searched])
                        limit_iter += 1
                        if limit_iter < len(self.limit):
                            timeLimit = time.time() + self.limit[limit_iter] / 1000

                else:
                    if len(self.node_searched) == self.limit[limit_iter]:
                        if self.best_node_till_now is None:
                            self.result[limit_iter].extend([None, None, self.jump_indicator, self.node_searched])
                        else:
                            self.result[limit_iter].extend([self.best_node_till_now.val, self.best_node_till_now.var_val, self.jump_indicator,self.node_searched])
                        limit_iter += 1
                if limit_iter >= len(self.limit):
                    return self.result
            temp_best_node = self.priority_queue.get_item()
            #print(temp_best_node.var_val)
            self.node_searched.append(temp_best_node.var_val)

            self.calculate_jump(temp_best_node,jump_level,temp_varval2)
            jump_level = temp_best_node.level
            temp_varval2 = temp_best_node.var_val.copy()

            if not temp_best_node.not_valid:
                if temp_best_node.is_final:  # if a valid solution then this is the best
                    if self.limitType != LimitType.unbounded:
                        while limit_iter < len(self.limit):
                            self.result[limit_iter].extend([temp_best_node.val, temp_best_node.var_val, self.jump_indicator, self.node_searched])
                            limit_iter += 1
                    self.result[-1]=[temp_best_node.val, temp_best_node.var_val, self.jump_indicator, self.node_searched]
                    return self.result
                    #return temp_best_node.val, temp_best_node.var_val, self.jump_indicator, self.node_searched
                else:  # otherwise, we're unsure if this branch holds promise. Maybe it can't actually achieve this lower bound. So branch into it
                    new_nodes = self.get_children(temp_best_node)
                    for new_node in new_nodes:
                        if new_node.is_final:
                            self.priority_queue.add(new_node,num)
                            num += 1
                        else:
                            res,new_val = self.get_lp_addition(new_node.var_val, new_node.level, new_node.get_problem())#self.lp_node_value(new_node.get_problem())
                            if res['success']:
                                new_node.val = new_val
                                if self.is_valid_solution(res['x']):
                                    new_node.is_final = True
                                    #print(f'var val {new_node.var_val}')
                                    for i,v in enumerate(res['x']):
                                        new_node.var_val[i+new_node.level] = int(v)
                                    if (self.best_node_till_now is None or self.best_node_till_now.val >= new_node.val):
                                        if self.limitType != LimitType.time:
                                            self.best_node_till_now = new_node
                                        elif time.time() <= timeLimit:
                                            self.best_node_till_now = new_node
                                        else:
                                            while time.time() > timeLimit and limit_iter < len(self.limit):
                                                if self.best_node_till_now is None:
                                                    self.result[limit_iter].extend([None, None, self.jump_indicator, self.node_searched])
                                                else:
                                                    self.result[limit_iter].extend([self.best_node_till_now.val, self.best_node_till_now.var_val, self.jump_indicator,self.node_searched])
                                                limit_iter += 1
                                                #timeLimit = time.time() + self.limit[limit_iter] / 1000
                                            if limit_iter < len(self.limit):
                                                timeLimit = time.time() + self.limit[limit_iter] / 1000
                                                self.best_node_till_now = new_node
                                    #print(f'new var val {new_node.var_val}')
                                    #new_node.var_val = res['x'] #res[LPResult.VAR_COEFF]
                                self.priority_queue.add(new_node,num)
                                num += 1
                            # else:
                            #     new_node.val = np.Infinity
                            #     new_node.is_final = True
                            #     new_node.not_valid = True
                        # heappush(heap, (res, next(counter), new_node))  # using counter to avoid possible comparisons between nodes. It tie breaks
        # no solution for this problem
        #return None, None, self.jump_indicator, self.node_searched
        self.result[-1]=[None, None, self.jump_indicator, self.node_searched]
        while limit_iter < len(self.limit):
            self.result[limit_iter].extend([None, None, self.jump_indicator, self.node_searched])
            limit_iter += 1
        return self.result
