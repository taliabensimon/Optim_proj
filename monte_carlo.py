import time
import math
import random
import numpy as np
import enum

class LimitType(enum.Enum):
    time = 0,
    turn = 1,
    unbounded = 2

def randomPolicy(state):
    visits = 1
    last_parent = state
    while not state.isTerminal():
        try:
            possible_actions = state.get_possible_actions()
            action = random.choice(possible_actions)
            visits += 1
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
        if not state.isTerminal():
            last_parent = state
    children_val = [c.val for c in last_parent.curr.children if c.val is not None]
    if len(children_val) == 2:
        val = min(children_val) if -np.inf not in children_val else max(children_val)
        last_parent.curr.set_final(val)
    return state.getReward(), visits

def random_fill_policy(state):
    return state.get_possible_solution(), 1

def weighted_policy(state):
    visits = 1
    last_parent = state
    while not state.isTerminal():
        try:
            prob_rate = [0.5,0.5]
            possible_actions = state.get_possible_actions()
            if len(possible_actions) == 2:
                if visits/2 >= len(state.curr.var_val):
                    val1 = possible_actions[0].node.h_val
                    val2 = possible_actions[1].node.h_val
                    if val1 is not None and val2 is not None:
                        if val2 > val1:
                            prob_rate =[0.6,0.4]
                        elif val2 < val1:
                            prob_rate = [0.4,0.6]
                    elif (val1 is not None and val2 is None ):
                        prob_rate = [0.2,0.8]
                    elif (val2 is not None and val1 is None ):
                        prob_rate = [0.8,0.2]

                chosen_action = np.random.choice(possible_actions, p=prob_rate)

            else:
                chosen_action = possible_actions[0]
            action = chosen_action#random.choice(possible_actions)
            visits += 1
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
        if not state.isTerminal():
            last_parent = state
    children_val = [c.val for c in last_parent.curr.children if c.val is not None]
    if len(children_val) == 2:
        val = min(children_val) if -np.inf not in children_val else max(children_val)
        last_parent.curr.set_final(val)
    return state.getReward(), visits


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isFullyExpanded = self.is_terminal()
        self.parent = parent
        self.num_visits = 0
        self.total_reward = 0
        self.best_reward = 0
        self.children = {}

    def is_terminal(self):
        return self.state.isTerminal()


class mcts():
    def __init__(self, solution, limit_arr = None, limit_type = 2, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy):
        self.max_lvl = 0
        self.total_visits = 0
        self.rollout_visits = 0
        self.solution = -solution
        self.limit_arr = limit_arr
        self.result = {k:[] for k in range(len(limit_arr))} if limit_arr is not None else {-1: []}
        self.limit_cell = 0
        self.limit_type = limit_type

        if LimitType(limit_type) == LimitType.time:
            self.timeLimit = np.array(self.limit_arr).max()
        elif LimitType(limit_type) == LimitType.turn:
            self.searchLimit = np.array(self.limit_arr).max()
        self.explorationConstant = explorationConstant
        self.rollout = random_fill_policy#weighted_policy##rolloutPolicy

    def search(self, initialState):

        self.curr_stamp = self.init_ts= time.time()
        self.turn = 0
        self.root = treeNode(initialState, None)
        if LimitType(self.limit_type) == LimitType.time:
            timeLimit = time.time() + self.timeLimit / 1000
            while time. time() < timeLimit and self.root.total_reward != self.solution and self.turn < 1000000:
                self.executeRound()
            self.fill_limit_cell(self.root.total_reward)
            print(f"Best Val {self.root.total_reward}")

        elif LimitType(self.limit_type) == LimitType.turn:
            for i in range(self.searchLimit):
                if self.turn in self.limit_arr:
                    self.update_limit_cell(self.root.total_reward)
                if self.root.total_reward == self.solution:
                    self.update_limit_cell(self.solution, id=-1)
                    break
                self.executeRound()
            self.fill_limit_cell(self.solution)
        else:
            i = 0
            while self.root.total_reward != self.solution:
                self.executeRound()
                i+=1
                if i == 1000000:
                    print("stopping after 1 mil turns")
                    break
        #bestChild = self.get_best_child(self.root, 0)
        print(f"rollout visits {self.rollout_visits} best val: {self.root.total_reward}")
        return (self.result if 0 in self.result and self.result[0] != [] else {-1:[self.root.total_reward, self.curr_stamp, self.rollout_visits + self.max_lvl, self.rollout_visits + self.total_visits]}), self.turn

    def update_limit_cell(self, reward, id = None):
        if id is not None:
            self.result[id] = [reward, self.curr_stamp - self.init_ts, self.rollout_visits + self.max_lvl,
                                            self.rollout_visits + self.total_visits]
        else:
            self.result[self.limit_cell] = [reward, self.curr_stamp - self.init_ts, self.rollout_visits + self.max_lvl, self.rollout_visits + self.total_visits]
            self.limit_cell += 1

    def fill_limit_cell(self, reward):
        for i in range(self.limit_cell,len(self.limit_arr)):
            self.result[i] = [reward, self.curr_stamp - self.init_ts, self.rollout_visits + self.max_lvl,
                                            self.rollout_visits + self.total_visits]

    def executeRound(self):
        self.turn += 1
        node = self.selectNode(self.root)
        if node.state.curr.not_valid:
            visits = 0
            reward = -np.inf
            # print("NODE SKIP")
        else:
            reward, visits = self.rollout(node.state)
            # print(f"rolling state {node.state.curr.var_val}")
        self.curr_stamp = time.time()
        delta_t = self.curr_stamp - self.init_ts
        # print(delta_t)
        if self.limit_type != LimitType.unbounded and self.limit_cell < len(self.limit_arr):
            if reward == self.solution:
                if self.limit_type == LimitType.time and self.limit_arr[self.limit_cell] >= delta_t:
                    self.update_limit_cell(reward)
                    self.fill_limit_cell(reward)
                else:
                    self.update_limit_cell(self.root.total_reward)
                    self.update_limit_cell(reward, id=-1)
            elif self.limit_type == LimitType.time and self.limit_arr[self.limit_cell] > delta_t:
                self.update_limit_cell(self.root.total_reward)
        self.rollout_visits += visits
        # print(f"reward {reward}, hval {node.state.curr.h_val}")
        self.backpropogate(node, reward)

    def selectNode(self, node):
        i=0
        self.total_visits += 1
        # for a in node.children.values():
        #     if a.state.curr.h_val is not None and a.state.curr.h_val > self.root.total_reward:
        #         a.state.curr.set_not_valid()
        #         a.total_reward = np.inf
        while not node.is_terminal():
            i+=1
            self.total_visits += 1
            if node.isFullyExpanded:
                node = self.get_best_child(node, self.explorationConstant)
                self.max_lvl = node.state.curr.level
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.get_possible_actions()

        for action in actions:
            if action not in node.children:
                new_node = treeNode(node.state.takeAction(action), node)
                if not new_node.state.curr.not_valid:
                    node.children[action] = new_node
                    # print(f"added {new_node.state.curr.val}")
                    if len(actions) == len(node.children):
                    #if len(actions) == node.state.get_num_explored_valid_children():
                        node.isFullyExpanded = True
                elif len(actions) == len(node.children) + 1:
                    node.isFullyExpanded = True
                return new_node
        # print(f"in children, node terminal {node.is_terminal()}")
        # print("EXCEPT")
        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        # print("IN BP")
        children_h_val = [c.h_val for c in node.state.curr.children if c.h_val is not None and c.h_val != -np.inf]
        if len(children_h_val) == 2:
            min_child_h_val = min([c.h_val for c in node.state.curr.children])
            if min_child_h_val != -np.inf:
                node.state.curr.h_val = min_child_h_val
                # if abs(self.root.state.curr.h_val - min_child_h_val) > 600:
                #     node.state.curr.set_not_valid()
        while node is not None:
            node.num_visits += 1
            # print(reward)
            if reward != -np.inf:
                # node.total_reward += reward
                # node.best_reward = min(reward, node.best_reward)
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
            # if child.total_reward < 0 and child.total_reward > self.root.total_reward:
            #     child.state.curr.set_not_valid()
            #     child.total_reward =np.inf
            h_val = child.state.curr.h_val if child.state.curr.h_val is not None else node.state.root.h_val
            # nodeValue = (child.total_reward) / child.num_visits + explorationValue * math.sqrt(2 * math.log(node.num_visits) / child.num_visits)
            nodeValue = (child.total_reward + h_val)/child.num_visits + explorationValue * math.sqrt(
                2 * math.log(node.num_visits) / child.num_visits)
            if nodeValue < bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        best_node = random.choice(bestNodes)
        return best_node