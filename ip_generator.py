from problem import *
import pickle
from bb import BranchAndBound
import numpy as np


def valid_problem(problem):
    b_b = BranchAndBound(problem)
    res = b_b.bbsolve()
    optim_val, optim_solution = res[0],res[1]
    if 1 not in optim_solution:
        return False, None
    if sum(optim_solution)<5:
        return False, None
    if optim_val is None:
        return False, None
    if np.dot(problem.original_func_coeff, optim_solution) != optim_val:
        return False, None
    for i,c in enumerate(problem.constraint_coeff):
        if np.dot(c,optim_solution) > problem.constraint_bound[i]:
            return False, None
    for i in optim_solution:
        if i not in [0,1]:
            return False, None
    return True, res

if __name__ == '__main__':
    num_of_data = 5
    problems = []
    ress1 = []
    while len(problems) <= num_of_data:
        func_coeff = []
        var_bounds = []
        const_coeff = []
        const_bound = []
        num_var = np.random.randint(20,50)
        const_num = int((100/max(num_var,15)) * 2)
        for i in range(num_var):
            func_coeff.append(np.random.randint(0,1000))
            var_bounds.append((0,1))
        for j in range(const_num):
            temp_arr = np.random.randint(0,100,size=num_var)
            temp_arr[np.random.choice(range(len(temp_arr)),size=int(len(temp_arr)//2))] = 0
            const_coeff.append(temp_arr)
            const_bound.append(np.random.randint(0,100))
        func_coeff = np.array(func_coeff) * -1
        prob = Problem(OptType.MIN, func_coeff, const_coeff, const_bound, var_bounds, func_coeff)
        v,res = valid_problem(prob)
        if v:
            problems.append(prob)
            ress1.append(res)
            np.random.seed(np.random.randint(0,2**32))

    with open("gen_problems_pickle2", "wb") as f:
        pickle.dump(problems, f)