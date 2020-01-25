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
