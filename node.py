from problem import Problem
import copy
import numpy as np

class Node(object):
    def __init__(self, var_vals, problem, val=None):
        self.var_val = var_vals
        self.problem = problem
        self.val = val
        self.heuristic_val = 0
        self.children = []
        self.is_final = None not in var_vals
        if not self.is_final:
            self.level = [i for i, val in enumerate(var_vals) if val == None][0]
        else:
            self.level = len(var_vals)
        self.not_valid = False
        if self.level >0:
            self.update_problem(problem)

    def add_child(self,child):
        self.children.append(child)

    def add_children(self,children):
        for child in children:
            self.add_child(child)

    def get_children(self):
        return self.children

    def set_val(self, val):
        self.val = val

    def get_val(self):
        return self.val

    def set_heuristic_val(self, val):
        self.heuristic_val = val

    def get_heuristic_val(self):
        return self.heuristic_val

    def update_problem(self, curr_problem):
        var_count = len(curr_problem.func_coeff)
        if self.is_final and not self.not_valid:  # if it's the last node
            self.val = np.dot(curr_problem.original_func_coeff, self.var_val)  #todo - still need to check if all bounds are meet
            return self.val

        func_coeff = np.zeros(var_count - self.level)
        for i, coeff in enumerate(curr_problem.func_coeff[self.level:]):#copy only coeff. from the next var and on
            func_coeff[i] = coeff

        const_coeff = []
        const_bound = []
        var_bound = []
        for i, ct in enumerate(curr_problem.constraint_coeff):
            var_val = ct[0] * self.var_val[self.level-1] # assign current variable it's value*it's coeff
            new_bound = curr_problem.constraint_bound[i] - var_val
            if len(ct) > 2:
                const_coeff.append([copy.deepcopy(ct[1:])])
                const_bound.append(new_bound)
            else:  # constraint becomes a variable bound
                bound = copy.deepcopy(curr_problem.var_bounds[self.level])
                if ct[1] < 0:  # sign changed => becomes a lower bound
                    lower_bound = new_bound
                    if bound[0] == None or abs(bound[0]) > abs(lower_bound):  # Update lower bound
                        bound[0] = lower_bound
                elif bound[1] == None or abs(bound[1]) > abs(new_bound):
                    bound[1] = new_bound
                var_bound.append(bound)
        self.problem = Problem(curr_problem.opt_type, func_coeff, const_coeff, const_bound, var_bound, curr_problem.original_func_coeff)

    def get_problem(self):
        return self.problem

    def get_level(self):
        return self.level