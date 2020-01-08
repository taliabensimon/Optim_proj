import scipy.optimize.linprog as scilp
import enum

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
    def lp_node_value(self, problem):
        result = scilp(problem.func_coeff, problem.constraint_coeff, problem.constraint_bound, problem.var_bounds)
        return result

    def get_next(self):
        pass

