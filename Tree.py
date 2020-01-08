import scipy.optimize.linprog as scilp
import enum
import numpy as np

class OptType(enum.Enum):
    MIN = 0,
    MAX = 1

class LPResult(enum.Enum):
    VAR_COEFF = 0,
    FUNC_VAL = 1,
    SLACKS_VAL = 2,
    CON = 3, #The (nominally zero) residuals of the equality constraints, b_eq - A_eq @ x
    SUCESS = 4,
    STATUS = 5,
    NUM_ITER = 6,
    MSG = 7

class Problem(object):
    def init(self, opt_type, func_coeff, constraint_coeff, constraint_bound, var_bounds):
        self.opt_type = opt_type
        self.func_coeff = func_coeff
        self.constraint_coeff = constraint_coeff
        self.constraint_bound = constraint_bound
        self.var_bounds = var_bounds



def lp_node_value(problem : Problem, node, curr_var):
    if curr_var == len(problem.func_coeff) - 1: # if it's the last node
        return sum(curr_var.var_val)

    func_coeff = np.zeros(problem.func_coeff-curr_var+1)
    for i,coeff in enumerate(problem.func_coeff[curr_var+1]):
        func_coeff[i] = coeff

    result = scilp(func_coeff, )
    return result

