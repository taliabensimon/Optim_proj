from scipy.optimize import linprog as scilp
import enum
from node import Node
import copy
import numpy as np

class LPResult(enum.Enum):
    VAR_COEFF = 0,
    FUNC_VAL = 1,
    SLACKS_VAL = 2,
    CON = 3, #The (nominally zero) residuals of the equality constraints, b_eq - A_eq @ x
    SUCESS = 4,
    STATUS = 5,
    NUM_ITER = 6,
    MSG = 7


class Tree(object):
    def __init__(self,problem):
        vars_val = [None] * len(problem.func_coeff)
        self.best_possible_val = self.lp_node_value(problem)['fun']
        self.root = Node(vars_val, problem, self.best_possible_val)

    def lp_node_value(self, problem):
        const_coeff = problem.constraint_coeff if len(problem.constraint_coeff) > 0 else None
        try:
            result = scilp(problem.func_coeff,A_ub = const_coeff,b_ub = problem.constraint_bound, bounds = problem.var_bounds)
        except:
            print("lp except")
            result = {
        'x': None,
        'fun': None,
        'slack': None,
        'con': None,
        'status': None,
        'message': None,
        'nit': None,
        'success': False}
        return result

    def get_lp_addition(self, var_vals, level, problem):
        val = np.inf
        addition = np.dot(var_vals[:level], problem.original_func_coeff[:level])
        result = copy.deepcopy(self.lp_node_value(problem))
        if result["success"]:
            val = result["fun"] + addition
        return result,val


    def is_valid_solution(self, x):
        #check if the solution contins only intergers
        return all(np.equal(np.mod(x, 1), 0)) #not False in np.eq...

    def get_children(self,node):
        if node.is_final:
            return None
        if len(node.children) > 0:
            return node.children
        prob1 = copy.deepcopy(node.get_problem())
        prob2 = copy.deepcopy(node.get_problem())
        vars_val_l = node.var_val.copy()
        vars_val_r = node.var_val.copy()
        vars_val_l[node.level] = 1
        left_n = Node(vars_val_l, prob1)
        vars_val_r[node.level] = 0
        right_n = Node(vars_val_r, prob2)
        node.add_children([left_n, right_n])
        return left_n, right_n

