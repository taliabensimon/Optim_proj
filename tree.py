import scipy.optimize.linprog as scilp
import enum
from node import Node

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
        self.best_possible_val = self.lp_node_value(problem)
        self.root = Node(vars_val, problem, self.best_possible_val)

    def lp_node_value(self, problem):
        result = scilp(problem.func_coeff, problem.constraint_coeff, problem.constraint_bound, problem.var_bounds)
        return result

    def get_children(self,node):
        if node.is_final():
            return None
        prob = node.get_problem()
        vars_val = node.var_val.copy()
        vars_val[node.level] = 1
        left_n = Node(vars_val, prob)
        vars_val[node.level] = 0
        right_n = Node(vars_val, prob)
        return left_n, right_n

