

class Node():
    def __init__(self, var_vals, problem, val=0):
        self.var_val = var_vals
        self.problem = problem
        self.update_problem(problem)
        self.val = val
        self.heuristic_val = 0
        self.children = []
        self.is_final = None not in var_vals
        if self.is_final:
            self.level = [i for i, val in enumerate(var_vals) if val == None][0] +1
        else:
            self.level = len(var_vals)


    def add_child(self,child):
        self.children.append(child)

    def add_children(self,children):
        for child in children:
            self.add_child(child)

    def get_children(self):
        return self.children

    def set_val(self, val):
        self.val = val

    def get_val(self):
        return self.val

    def set_heuristic_val(self, val):
        self.heuristic_val = val

    def get_heuristic_val(self):
        return self.heuristic_val

    def update_problem(self):
        self.problem = 1  # todo

    def get_problem(self):
        return self.problem

    def is_final(self):
        return self.is_final()

    def get_level(self):
        return self.level