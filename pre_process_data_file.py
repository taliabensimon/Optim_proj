import numpy as np
from problem import  *
import pickle

if __name__ == '__main__':
    files = ["mknap1.txt"]# + [f"mknapcb{i}.txt" for i in range(1,10)]
    problems = []
    for file in files:
        with open(file,"r") as f:
            content = f.read().split("\n\n ")[1].split("\n \n")#skip first line which indicates number of problems in file
        for problem in content:
            if problem.strip() == "":
                continue
            problem = problem.strip().split("\n ")
            num_vars, num_consts, opt_sol = np.array(problem[0].split(" "), dtype=float)
            if opt_sol == 0: # indicates that solution is unavailable
                continue
            func_coeff = np.array(problem[1].split(" "), dtype=float)*-1
            var_bound = [(0,1) for f in range(len(func_coeff))]

            const_coeff = []
            const_bound = []

            for i in range(2,2+int(num_consts)):
                const_coeff.append(np.array(problem[i].split(" "), dtype=float))

            assert len(const_coeff) == int(num_consts)
            const_bound = np.array(problem[2+int(num_consts)].split(" "), dtype=float)
            problems.append(Problem(OptType.MIN, func_coeff, const_coeff, const_bound, var_bound, func_coeff))
    with open("problems_pickle", "wb") as f:
        pickle.dump(problems, f)



