from problem import Problem
import copy
import numpy as np

class Node(object):
    def __init__(self, var_vals, problem, val=None):
        self.var_val = var_vals
        self.problem = problem
        self.val = val
        self.h_val = None
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
        self.children.extend(children)

    def eval_children(self):
        if self.is_final:
            return None
        prob1 = copy.deepcopy(self.get_problem())
        prob2 = copy.deepcopy(self.get_problem())
        vars_val_l = self.var_val.copy()
        vars_val_r = self.var_val.copy()
        vars_val_l[self.level] = 1
        left_n = Node(vars_val_l, prob1)
        vars_val_r[self.level] = 0
        right_n = Node(vars_val_r, prob2)
        self.add_children([left_n, right_n])
        return left_n, right_n

    def get_children(self):
        if len(self.children) == 0:
            self.eval_children()
        assert len(self.children) <= 2
        children_h_val = [c.h_val for c in self.children if c.h_val is not None and c.h_val != -np.inf]
        if len(children_h_val) == 2:
            min_child_h_val = min([c.h_val for c in self.children])
            if min_child_h_val != -np.inf:
                self.h_val = min_child_h_val
        return self.children

    def set_val(self, val):
        self.val = val

    def get_val(self):
        return self.val

    def set_heuristic_val(self, val):
        self.heuristic_val = val

    def get_heuristic_val(self):
        return self.heuristic_val

    def is_var_in_bounds(self, value, bound):
        return value <= bound[1] and value >= bound[0]

    def set_not_valid(self):
        self.not_valid = True
        self.is_final = True
        self.h_val = -np.inf
        self.val = -np.inf

    def set_final(self, val):
        self.is_final = True
        self.val = val

    def update_problem(self, curr_problem):
        if self.is_final and not self.not_valid: # if it's the last node and it's valid
            if self.is_var_in_bounds(self.var_val[-1], curr_problem.var_bounds[0]):
                self.val = np.dot(curr_problem.original_func_coeff, self.var_val)
            else:
                self.set_not_valid()

        func_coeff = copy.deepcopy(curr_problem.func_coeff[1:])#copy only coeff. from the next var and on
        var_bound = copy.deepcopy(curr_problem.var_bounds[1:])

        const_coeff = []
        const_bound = []

        for i, ct in enumerate(curr_problem.constraint_coeff):
            var_assignment = ct[0] * self.var_val[self.level-1] # assign current variable it's value*it's coeff
            new_bound = curr_problem.constraint_bound[i] - var_assignment
            if len(ct) > 2:
                const_coeff.append(copy.deepcopy(ct[1:]))
                const_bound.append(new_bound)
            else:  # constraint becomes a variable bound
                bound = list(var_bound[0])
                if ct[1] == 0:
                    if var_assignment > curr_problem.constraint_bound[i]:
                          self.set_not_valid()
                          break
                    else:
                        continue
                new_bound /= ct[1]

                if (ct[1] < 0 and new_bound > bound[1]) or new_bound < bound[0]:
                    self.set_not_valid()
                    break
                elif ct[1] < 0:  # sign changed => becomes a lower bound
                    lower_bound = new_bound

                    if bound[0] == None or abs(bound[0]) > abs(lower_bound):  # Update lower bound
                        bound[0] = lower_bound
                elif bound[1] == None or abs(bound[1]) > abs(new_bound):
                    bound[1] = new_bound
                var_bound[-1] = tuple(bound) # only when the last variable left a constraint becomes a bound
        # if len(const_coeff) == 0:
        #     self.is_final = True
        self.problem = Problem(curr_problem.opt_type, func_coeff, const_coeff, const_bound, var_bound, curr_problem.original_func_coeff)

    def get_problem(self):
        return self.problem

    def get_level(self):
        return self.level

