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

            i = 1
            func_coeff = np.array(problem[i].split(" "), dtype=float)*-1
            while len(func_coeff) < num_vars:
                i+=1
                func_coeff = np.concatenate((func_coeff, np.array(problem[i].split(" "), dtype=float) * -1))
            i+=1
            var_bound = [(0,1) for f in range(len(func_coeff))]

            const_coeffs = []
            const_bound = []
            j = i
            for _ in range(i,i+int(num_consts)):
                const_coeff = np.array(problem[j].split(" "), dtype=float)

                while len(const_coeff) < num_vars:
                    j+=1
                    const_coeff = np.concatenate((const_coeff, np.array(problem[j].split(" "), dtype=float)))
                j+=1
                const_coeffs.append(const_coeff)


            assert len(const_coeffs) == int(num_consts)
            const_bound = np.array(problem[j].split(" "), dtype=float)
            problems.append((Problem(OptType.MIN, func_coeff, const_coeffs, const_bound, var_bound, func_coeff), opt_sol))
    with open("problems_pickle_v2", "wb") as f:
        pickle.dump(problems, f)



