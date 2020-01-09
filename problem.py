import enum

class Problem(object):
    #At some point, make this immutable - such that changing an attribute, returns a new class
    def init(self, opt_type, func_coeff, constraint_coeff, constraint_bound, var_bounds, original_func_coeff):
        self.original_func_coeff = original_func_coeff
        self.opt_type = opt_type
        self.func_coeff = func_coeff
        self.constraint_coeff = constraint_coeff
        self.constraint_bound = constraint_bound
        self.var_bounds = var_bounds


class OptType(enum.Enum):
    MIN = 0,
    MAX = 1
