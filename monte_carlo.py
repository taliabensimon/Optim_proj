import time
import math
import random
import numpy as np

def randomPolicy(state):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isFullyExpanded = self.is_terminal()
        self.parent = parent
        self.num_visits = 0
        self.total_reward = 0
        self.children = {}

    def is_terminal(self):
        return self.state.isTerminal()


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState):
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()
        bestChild = self.get_best_child(self.root, 0)
        while len(bestChild.children) > 0:
            bestChild = self.get_best_child(bestChild, 0)
        return bestChild

    def executeRound(self):
        node = self.selectNode(self.root)
        print(f"rolling state {node.state.curr.var_val}")
        reward = self.rollout(node.state)
        print(f"reward {reward}")
        self.backpropogate(node, reward)

    def selectNode(self, node):
        i=0
        while not node.is_terminal():
            i+=1
            if node.isFullyExpanded:
                node = self.get_best_child(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()

        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                print(f"added {newNode.state.curr.val}")
                if len(actions) == len(node.children):
                #if len(actions) == node.state.get_num_explored_valid_children():
                    node.isFullyExpanded = True
                return newNode
        # print(f"in children, node terminal {node.is_terminal()}")
        # print("EXCEPT")
        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        # print("IN BP")
        while node is not None:
            node.num_visits += 1
            # print(reward)
            if reward != -np.inf:
                #node.total_reward += reward
                node.total_reward = min(reward, node.total_reward)
            else:
                if not node.state.has_valid_child():
                    # print("IN NO VALID CHILD")
                    # print(f"node terminal {node.is_terminal()}")
                    node.state.curr.not_valid = True
                    node.isFullyExpanded = True
                    node.state.curr.val = -np.inf
                    node.total_reward = -np.inf
                else:
                    k_to_remove = None
                    for (k,v) in node.children.items():
                        if v.state.curr.not_valid:
                            k_to_remove = k
                            break
                    node.children = {key: val for key, val in node.children.items() if key != k_to_remove}
            node = node.parent

    def get_best_child(self, node, explorationValue):
        # choices_weights = [
        #     (-child.total_reward / child.num_visits) +
        #     explorationValue * np.sqrt((2 * np.log(node.num_visits) / child.num_visits))
        #     for child in node.children.values()]
        # return node.children.items()[np.argmax(choices_weights)]
        bestValue = np.inf
        bestNodes = []
        for child in node.children.values():
            if child.total_reward == -np.inf:
                continue
            h_val = child.state.curr.h_val if child.state.curr.h_val is not None else 0
            # nodeValue = (child.total_reward + h_val/2) / child.num_visits + explorationValue * math.sqrt(2 * math.log(node.num_visits) / child.num_visits)
            nodeValue = (child.total_reward + h_val / 2)/child.num_visits #+ explorationValue * math.sqrt(
                #2 * math.log(node.num_visits) / child.num_visits)
            if nodeValue < bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        best_node = random.choice(bestNodes)
        return best_node