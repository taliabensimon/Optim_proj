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
    def init(self, opt_type, func_coeff, constraint_coeff, constraint_bound, var_bounds):
        self.opt_type = opt_type
        self.func_coeff = func_coeff
        self.constraint_coeff = constraint_coeff
        self.constraint_bound = constraint_bound
        self.var_bounds = var_bounds



def lp_node_value(problem : Problem, node, curr_var):
    '''

    :param problem: current subtree problem
    :param node: current node
    :param curr_var: index of the variable that is being assigned
    :return:
    '''
    var_count = len(problem.func_coeff)
    if curr_var == var_count - 1: # if it's the last node
        return sum(node.var_val)

    func_coeff = np.zeros(var_count-curr_var+1)
    for i,coeff in enumerate(problem.func_coeff[curr_var+1]):
        func_coeff[i] = coeff

    const_coeff = []
    const_bound = []
    var_bound = []
    for i,ct in enumerate(problem.constraint_coeff):
        var_val = const_bound[i]-ct[0]*node.var_val
        new_bound = problem.constraint_bound[i] - var_val
        if len(ct) > 2:
            const_coeff.append([ct[1:]])
            const_bound.append(new_bound)
        else: #constraint becomes a variable bound
            bound = copy.deepcopy(problem.var_bounds[curr_var+1])
            if ct[1] < 0: # sign changed => becomes a lower bound
                lower_bound = new_bound
                if bound[0] == None or abs(bound[0]) > abs(lower_bound): # Update lower bound
                    bound[0] = lower_bound
            elif bound[1] == None or abs(bound[1]) > abs(new_bound):
                bound[1] = new_bound
            var_bound.append(bound)

    result = scilp(func_coeff, const_coeff, const_bound, var_bound)
    return result

