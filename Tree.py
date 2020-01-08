import scipy.optimize.linprog as scilp
import enum
import numpy as np
import copy

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
    #At some point, make this immutable - such that changing an attribute, returns a new class
    def init(self, opt_type, func_coeff, constraint_coeff, constraint_bound, var_bounds, original_func_coeff):
        self.original_func_coeff = original_func_coeff
        self.opt_type = opt_type
        self.func_coeff = func_coeff
        self.constraint_coeff = constraint_coeff
        self.constraint_bound = constraint_bound
        self.var_bounds = var_bounds



def lp_node_value(problem):
    result = scilp(problem.func_coeff, problem.constraint_coeff, problem.constraint_bound, problem.var_bounds)
    return result

