import os
from problem import Problem, OptType
from bip_state import BinaryIntegerProgramming as BIP
from monte_carlo import mcts, LimitType
from node import Node
from  bb import BranchAndBound
import pickle
import numpy as np
from graphs import graph_for_size

def call_bb(p,arr_limits,type):
    b_b = BranchAndBound(p,type,arr_limits)
    res = b_b.bbsolve()
    # print(f'solution value: {res[0]}, vars_solution: {res[1]}')
    # print(f'node searched: {res[3]}')
    # print(f'jumps: {res[2]}')
    return res #todo- return vals for graphs

def call_mcts(p,v,arr_limits,type):
    vars_val = [None] * len(p.func_coeff)
    root = Node(vars_val, p)
    bip = BIP(root, None)
    mc = mcts(v, arr_limits, type)
    res = mc.search(bip)
    # print(res)
    # print(res.total_reward)
    # print(f'problem {i + 1} solution is {v} mc solution is {res.total_reward}')
    return res  # todo- return vals for graphs

def get_avrg_dict(dict_arr,sub=0):
    result = {}
    for d in dict_arr:
        for k in d.keys():
            result[k] = result.get(k, 0) + d[k] - sub
    for k in result.keys():
        result[k] /= len(dict_arr)
    return result


if __name__ == '__main__':
    num_avrg_mcts = 5
    problems_size = [50,100,500]
    arry_type = [LimitType.unbounded, LimitType.time,LimitType.turn]
    arry_limit = [None, [50,100,150,200,250,300,350,400,450,500], [1,2,3,4,5,7,10,15,22,30,40,55,70,90,140,200,300,450,700,1000,1500,3000]]
    with open("problems_pickle_v2", 'rb') as f:
        problems_arr = pickle.load(f)
    for j,p_size in enumerate(problems_size):
        size_res = []

        for ij,arr in enumerate(arry_limit): #todo - case -1 unbounded (base)
            size_res_bb = []
            size_res_mtc = []

            for i, (p, v) in enumerate(problems_arr):
                low_lim = 0 if j == 0 else problems_size[j - 1]
                if p.func_coeff <= p_size and p.func_coeff > low_lim:
                    continue

                res_bb = call_bb(p,arr,arry_type[ij])
                res_mtc = []
                for mc_t in range(num_avrg_mcts):
                    res_mtc.append(call_mcts(p, v, arr, arry_type[ij]))
                res_mtc = get_avrg_dict(res_mtc,v)

                for k in res_bb.keys():
                    res_bb[k] -= v

                size_res_bb.append(res_bb)
                size_res_mtc.append(res_mtc)

                print('_______________________________________________________\n\n\n\n')
            size_res_mtc = get_avrg_dict(size_res_mtc)
            size_res_bb = get_avrg_dict(size_res_bb)
            graph_for_size(arry_type[ij],arr,size_res_bb.values(),size_res_mtc.values(),p_size)
