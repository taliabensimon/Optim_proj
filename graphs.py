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
    if prob_size is None:
        plt.plot(arr, res_bb, 'b', label='bb')
        plt.plot(arr, res_mct[0], 'r', label='mct')
        plt.xlabel('problem size')
        plt.ylabel('avrg num of nodes seen')
        plt.title('avrg num of nodes seenfor problem size')
        plt.show()
        plt.plot(arr, res_bb, 'b', label='bb')
        plt.plot(arr, res_mct[1], 'r', label='mct')
        plt.xlabel('problem size')
        plt.ylabel('avrg num of turns')
        plt.title(f'avrg num of turns seenfor problem size')
        plt.show()
    else:
        plt.plot(arr,res_bb,'b',label='bb')
        plt.plot(arr, res_mct, 'r',label='mct')
        plt.xlabel(f'{limit_type}')
        plt.ylabel('dist from optimal')
        plt.title(f'problem size: {prob_size},limit type: {limit_type}')
        plt.show()
