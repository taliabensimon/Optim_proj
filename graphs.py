import matplotlib.pyplot as plt

def graph(problem_size, prob):
    map = {}
    if len(prob[1]) == problem_size:
        for k,v in prob[2].items():
            map[k] = map.get(k, v) + v

    x = []
    y = []
    for k, v in map.items():
        if k ==0 :
            continue
        x.append(k)
        y.append(v)
    plt.hist(x,weights=y)
    plt.title(f'problem size: {problem_size}')
    plt.show()

def graph_for_size(limit_type,arr,res_bb,res_mct,prob_size):
    plt.plot(arr,res_bb,'b',label='bb')
    plt.plot(arr, res_mct, 'r',label='mct')
    plt.xlabel(f'{limit_type}')
    plt.ylabel('dist from optimal')
    plt.title(f'problem size: {prob_size},limit type: {limit_type}')
    plt.show()
    return
