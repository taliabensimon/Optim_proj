import numpy as np
from problem import  *
import pickle

def mknap1():
    problems = []
    with open("mknap1.txt", "r") as f:
        content = f.read().split("\n\n ")[1].split(
            "\n \n")  # skip first line which indicates number of problems in file
    for problem in content:
        if problem.strip() == "":
            continue
        problem = problem.strip().split("\n ")
        num_vars, num_consts, opt_sol = np.array(problem[0].split(" "), dtype=float)
        if opt_sol == 0:  # indicates that solution is unavailable
            continue

        i = 1
        func_coeff = np.array(problem[i].split(" "), dtype=float) * -1
        while len(func_coeff) < num_vars:
            i += 1
            func_coeff = np.concatenate((func_coeff, np.array(problem[i].split(" "), dtype=float) * -1))
        i += 1
        var_bound = [(0, 1) for f in range(len(func_coeff))]

        const_coeffs = []
        const_bound = []
        j = i
        for _ in range(i, i + int(num_consts)):
            const_coeff = np.array(problem[j].split(" "), dtype=float)

            while len(const_coeff) < num_vars:
                j += 1
                const_coeff = np.concatenate((const_coeff, np.array(problem[j].split(" "), dtype=float)))
            j += 1
            const_coeffs.append(const_coeff)

        assert len(const_coeffs) == int(num_consts)
        const_bound = np.array(problem[j].split(" "), dtype=float)
        problems.append(
            (Problem(OptType.MIN, func_coeff, const_coeffs, const_bound, var_bound, func_coeff), opt_sol))
    with open("problems_pickle_v2", "wb") as f:
        pickle.dump(problems, f)

def mknapcb():
    problems = []
    files = [f"mknapcb{i}.txt" for i in range(1, 10)]
    for f_id, file in enumerate(files):
        with open(file) as f:
            content = f.readlines()
        num_problems = int(content[0][:-1])
        i=1
        for _ in range(num_problems):
            num_vars, num_consts, opt_sol = np.array(content[i][:-1].strip().split(" "), dtype=float)
            i+=1
            func_coeff = np.array(content[i][:-1].strip().split(" "), dtype=float) * -1
            while len(func_coeff) < num_vars:
                i += 1
                func_coeff = np.concatenate((func_coeff, np.array(content[i][:-1].strip().split(" "), dtype=float) * -1))
            i += 1
            assert len(func_coeff) == num_vars
            var_bound = [(0, 1) for f in range(len(func_coeff))]

            const_coeffs = []

            j = i
            for _ in range(i, i + int(num_consts)):
                const_coeff = np.array(content[j][:-1].strip().split(" "), dtype=float)

                while len(const_coeff) < num_vars:
                    j += 1
                    const_coeff = np.concatenate((const_coeff, np.array(content[j][:-1].strip().split(" "), dtype=float)))
                j += 1
                const_coeffs.append(const_coeff)
            assert len(const_coeffs) == int(num_consts)

            const_bound = np.array(content[j][:-1].strip().split(" "), dtype=float)
            while len(const_bound) < len(const_coeffs):
                j += 1
                const_bound = np.concatenate((const_bound, np.array(content[j][:-1].strip().split(" "), dtype=float)))
            j += 1
            assert len(const_bound) == int(num_consts)

            i = j
            problems.append((Problem(OptType.MIN, func_coeff, const_coeffs, const_bound, var_bound, func_coeff), opt_sol))
        with open(f"problems_mknapcb{f_id+1}_pickle", "wb") as f:
            pickle.dump(problems, f)


if __name__ == '__main__':
    # mknap1()
    mknapcb()


