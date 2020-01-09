from heapq import *
from tree import Tree
from node import Node


class MaxHeap(object):

    def __init__(self):
        self.priority_queue = []

    def add(self,data):
        for i in data:
            item = (-i.val, i)
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
    def __init__(self):
        self.priority_queue = MaxHeap()

    def heuristic(self):
        # a basic heuristic of taking the ones it seems pretty sure about
        return min([(min(1 - v.value, v.value), i, v) for i, v in enumerate(self.bool_vars)])[2]

    def bbsolve(self):
        self.priority_queue.add([(self.best_possible_val, self.root)])
        bestres = 1e20  # a big arbitrary initial best objective value
        bestnode = root  # initialize bestnode to the root
        nodecount = 0
        while len(heap) > 0:
            nodecount += 1  # for statistics
            print("Heap Size: ", len(heap))
            _, _, node = heappop(heap)
            prob = node.buildProblem()
            res = prob.solve()
            print("Result: ", res)
            if prob.status not in ["infeasible", "unbounded"]:
                if res > bestres - 1e-3:  # even the relaxed problem sucks. forget about this branch then
                    print("Relaxed Problem Stinks. Killing this branch.")
                    pass
                elif node.is_integral():  # if a valid solution then this is the new best
                    print("New Best Integral solution.")
                    bestres = res
                    bestnode = node
                else:  # otherwise, we're unsure if this branch holds promise. Maybe it can't actually achieve this lower bound. So branch into it
                    new_nodes = node.branch()
                    for new_node in new_nodes:
                        heappush(heap, (res, next(counter),
                                        new_node))  # using counter to avoid possible comparisons between nodes. It tie breaks
        print("Nodes searched: ", nodecount)
        return bestres, bestnode