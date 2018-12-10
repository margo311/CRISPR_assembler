
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import pickle
import editdistance as ed

class Component:
    def __init__(self):
        self.chain = []
    
    def add_edge(self, edge):
        if len(self.chain) == 0:
            self.chain.append(edge[0])
            self.chain.append(edge[1])
            return True
        elif edge[0] == self.chain[-1]:
            self.chain.append(edge[1])
            return True
        elif edge[1] == self.chain[0]:
            self.chain.insert(0, edge[0])
            return True
        else:
            return False
        
        
    def allow_edge(self, edge):
        if len(self.chain) == 0:
            return True
        elif not edge[0] in self.chain[:-1] and not edge[1] in self.chain[1:] and not (edge[0] == self.chain[-1] and edge[1] == self.chain[0]):
            return True
        else:
            return False
    
    def require_edge(self, edge):
        if not self.allow_edge(edge):
            return False
        if edge[0] == self.chain[-1]:
            return True
        if edge[1] == self.chain[0]:
            return True
        
    def merge(self, component):
        if component.chain[0] == self.chain[-1]:
            self.chain.extend(component.chain[1:])
            return True
        elif component.chain[-1] == self.chain[0]:
            new_chain = component.chain
            new_chain.extend(self.chain[1:])
            self.chain = new_chain
            return True
        else:
            return False
        
    def __str__(self):
        return str(self.chain)
    
    def __repr__(self):
        return str(self.chain)



def restore_arrays(graph, threashold = 0):
    components = {}
    name = 0
    for argmax in graph.flatten().argsort()[::-1]:
        edge = (argmax // graph.shape[0], argmax % graph.shape[0])
        if graph[edge[0], edge[1]] > threashold:
        #print(edge, len(components))
            if len(components) == 0:
                c = Component()
                c.add_edge(edge)
                components[name] = c
                name += 1
                #break
            else:
                if all([comp.allow_edge(edge) for comp in components.values()]):
                    require_names = [name for name in components if components[name].require_edge(edge)]
                    #print("rn", require_names)
                    if len(require_names) == 0:
                        c = Component()
                        c.add_edge(edge)
                        components[name] = c
                        name += 1
                        #break
                    elif len(require_names) == 1:
                        components[require_names[0]].add_edge(edge)
                        #break
                    elif len(require_names) == 2:
                        components[require_names[0]].add_edge(edge)
                        components[require_names[0]].merge(components[require_names[1]])
                        components.pop(require_names[1])
                        #break
    weights = []
    comps_as_list = []
    
    for comp in components.values():
        comps_as_list.append(comp.chain)
        curr_weights = []
        for a,b in zip(comp.chain, comp.chain[1:]):
            curr_weights.append(graph[a][b])
        weights.append(curr_weights)
        
    return comps_as_list, weights
    

def comp_to_gr(components, spacers_num, o_gr = None):
    gr = np.zeros((spacers_num, spacers_num))
    
    for k in components.keys():
        for a,b in zip(components[k].chain, components[k].chain[1:]):
            if not o_gr is None:
                if o_gr[a][b] > 0:
                    gr[a][b] = 1
            else:
                gr[a][b] = 1
    
    return gr

def list_to_gr(components, spacers_num, o_gr = None):
    gr = np.zeros((spacers_num, spacers_num))
    
    for k in components:
        for a,b in zip(k, k[1:]):
            if not o_gr is None:
                if o_gr[a][b] > 0:
                    gr[a][b] = 1
            else:
                gr[a][b] = 1
    
    return gr

def pairs_to_gr(pairs, spacers_num):
    gr = np.zeros((spacers_num, spacers_num))
    
    for p in pairs:
        gr[p[0]][p[1]] += 1
    
    return gr

def a_in_b(a,b):
    a = np.array(a)
    b = np.array(b)
    if len(a) > len(b):
        return False
    else:
        for i in range(len(b) - len(a) + 1):
            if all(b[i:i + len(a)] == a):
                return True
    return False

def a_in_any_b(a,b):
    return any([a_in_b(a, x) for x in b])



def a_close_to_b(a, b, t = 2):
    return ed.eval(a, b) <= 2

def a_close_to_any_b(a, b, t = 2):
    return any([a_close_to_b(a, x, t) for x in b])
        



def elongate_chain(gr, chain):
    suggested_edges = []
    argmax = np.argmax(gr[:, chain[0]])
    if gr[argmax, chain[0]] > 0:
        return argmax
    else:
        return -1
    
def elongate_chains(gr, chains):
    for chain in chains: 
        suggested = elongate_chain(gr, chain)
        if suggested != -1:
            print([suggested] + chain)
        else:
            print(chain)



def solve_gready(inp_gr):
    spacers_num = inp_gr.shape[0]
    components = {}
    name = 0
    
    name = next_edge(inp_gr, components, name)
    
    return comp_to_gr(components, spacers_num, inp_gr), components




def split(chain, weights):
    splits = np.where(weights == 0)[0] 
    return np.split(chain, splits + 1), np.split(weights, splits)


def search_best_alignment(a, b, t = 2):
    answ = ('', '')
    indexes = (-1,-1,-1,-1)
    b_index = -1
    
    for i, x in enumerate(b):
        curr_answ, curr_indexes = best_alignment(a, x, t)
        if len(curr_answ[0]) >= len(answ[0]) and len(curr_answ[1]) >= len(answ[1]):
            answ = curr_answ
            indexes = curr_indexes
            b_index = i
        curr_answ, curr_indexes = best_alignment(a[::-1], x, t)
        if len(curr_answ[0]) >= len(answ[0]) and len(curr_answ[1]) >= len(answ[1]):
            answ = curr_answ
            indexes = curr_indexes
            b_index = i
        
    return answ, b_index, indexes


def best_alignment(a, b, t):
    '''worst implementation of best alignment ever'''
    answ = ('','')
    i1a, i2a, j1a, j2a = -1,-1,-1,-1
    for i1 in range(0, len(a)):
        for i2 in range(i1 + 1, len(a) + 1):
            check_a = a[i1:i2]
            for j1 in range(0, len(b)):
                for j2 in range(j1 + 1,  len(b) + 1):
                    check_b = b[j1:j2]
                    if ed.eval(check_a, check_b) <= t and len(check_a) >= len(answ[0]) and len(check_b) >= len(answ[1]):
                        answ = (check_a, check_b)
                        i1a, i2a, j1a, j2a = i1,i2,j1,j2
    
    return answ, (i1a,i2a,j1a,j2a)

    



