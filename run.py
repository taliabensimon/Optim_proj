import os
from problem import Problem, OptType
from bip_state import BinaryIntegerProgramming as BIP
from monte_carlo import mcts, LimitType
from node import Node
from  bb import BranchAndBound
import pickle
import numpy as np
from graphs import graph_for_size
import atexit

def call_bb(p,arr_limits,type):
    b_b = BranchAndBound(p,type,arr_limits)
    res = b_b.bbsolve()
    # print(f'solution value: {res[0]}, vars_solution: {res[1]}')
    # print(f'node searched: {res[3]}')
    # print(f'jumps: {res[2]}')
    return res #todo- return vals for graphs

def call_mcts(p,v,arr_limits,type,get_num=False):
    vars_val = [None] * len(p.func_coeff)
    root = Node(vars_val, p)
    bip = BIP(root, None)
    mc = mcts(v, arr_limits, type)
    res,num = mc.search(bip)
    # print(res)
    # print(res.total_reward)
    # print(f'problem {i + 1} solution is {v} mc solution is {res.total_reward}')
    if get_num:
        return res,num  # todo- return vals for graphs
    return res

def get_avrg_dict(dict_arr,sub=0,t=True):
    result = {}
    for d in dict_arr:
        for k in d.keys():
            if t:
                result[k] = result.get(k, 0) + abs(d[k][0] + sub)
            else:
                result[k] = result.get(k, 0) + abs(d[k] + sub)
    for k in result.keys():
        result[k] /= len(dict_arr)
    return result


if __name__ == '__main__':
    num_avrg_mcts = 1
    problems_size = [50,100,500]
    arry_type = [LimitType.time,LimitType.turn]
    #time_arr = [i for i in range(100,1000,100)].append([i for i in range(1000,10000,500)]).append([i for i in range(10000,60000,1000)]).append([i for i in range(60000,350000,10000)])
    arry_limit = [[50,100,150,200,250,300,350,400,450,500], [1,2,3,4,5,7,10,15,22,30,40,55,70,90,140,200,300,450,700,1000,1500,3000]]
    with open("problems_large_data_pickle", 'rb') as f:
        problems_arr = pickle.load(f)
    with open("problems_pickle_v2", 'rb') as f:
        problems_arr.extend(pickle.load(f))

    turns_map_bb = {}
    num_turns_map_bb = {}
    turns_map_mc = {}
    num_turns_map_mc = {}
    turns_map_mc2 = {}
    for i, (p, v) in enumerate(problems_arr):
        if len(p.func_coeff) > 6 or i == 23 or i == 5 or i == 6:
            continue
        print(i)
        res_bb = call_bb(p, None, LimitType.unbounded)
        print("------finish unbound bb-------\n\n")
        res_mtc = []
        res_mc_num = 0
        for mc_t in range(num_avrg_mcts):
            res_t,num_t = call_mcts(p, v, None, LimitType.unbounded,True)
            print("------finish unbound mc-------\n\n")
            res_mtc.append(res_t)
            res_mc_num += num_t
        res_mtc = get_avrg_dict(res_mtc)
        res_mc_num /= num_avrg_mcts
        turns_map_bb[len(p.func_coeff)] = turns_map_bb.get(len(p.func_coeff), 0) + len(res_bb[-1][3])
        num_turns_map_bb[len(p.func_coeff)] = num_turns_map_bb.get(len(p.func_coeff), 0) + 1
        turns_map_mc[len(p.func_coeff)] = turns_map_mc.get(len(p.func_coeff), 0) + res_mtc[-1][3]
        turns_map_mc2[len(p.func_coeff)] = turns_map_mc2.get(len(p.func_coeff), 0) + res_mc_num
        num_turns_map_mc[len(p.func_coeff)] = num_turns_map_mc.get(len(p.func_coeff), 0) + 1

    for k in turns_map_bb.keys():
        turns_map_bb[k] /= num_turns_map_bb[k]
        turns_map_mc[k] /= num_turns_map_mc[k]
        turns_map_mc2[k] /= num_turns_map_mc[k]

    graph_mc = list(turns_map_mc.values()).append(list(turns_map_mc2.values()))
    graph_for_size(LimitType.unbounded,list(turns_map_bb.keys()),list(turns_map_bb.values()),graph_mc,None)

    for j,p_size in enumerate(problems_size):
        size_res = []

        for ij,arr in enumerate(arry_limit):
            size_res_bb = []
            size_res_mtc = []

            for i, (p, v) in enumerate(problems_arr):
                if i == 23 or i == 5 or i == 6:
                    continue
                low_lim = 0 if j == 0 else problems_size[j - 1]
                if len(p.func_coeff) < p_size and len(p.func_coeff) >= low_lim:
                    print(i)

                    res_bb = call_bb(p,arr,arry_type[ij])
                    print("------finish unbound bb-------\n\n")
                    res_mtc = []
                    for mc_t in range(num_avrg_mcts):
                        res_mtc.append(call_mcts(p, v, arr, arry_type[ij]))
                        print("------finish unbound mc-------\n\n")
                    res_mtc = get_avrg_dict(res_mtc,v)

                    for k in res_bb.keys():
                        temp_aq = 0 if res_bb[k][0] is None else res_bb[k][0]
                        res_bb[k] = abs(temp_aq + v)

                    size_res_bb.append(res_bb)
                    size_res_mtc.append(res_mtc)

                    print('_______________________________________________________\n\n\n\n')
                else:
                    continue
            size_res_mtc = get_avrg_dict(size_res_mtc,t=False)
            size_res_bb = get_avrg_dict(size_res_bb,t=False)
            size_res_mtc.pop(-1, None)

            size_res_bb.pop(-1, None)
            graph_for_size(" turns",arr,list(size_res_bb.values()),list(size_res_mtc.values()),p_size)
