from heapq import *
from Tree import Tree


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


class BranchAndBound(Tree):
    def __init__(self):
        self.priority_queue = []