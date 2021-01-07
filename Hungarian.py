# ΕΧΕΙ ERRORS ΓΙΑΤΙ ΠΡΕΠΕΙ ΝΑ ΒΑΛΕΙΣ ΤΟ ΔΙΚΟ ΣΟΥ ΠΙΝΑΚΑ ΚΟΣΤΟΥΣ (ΟΠΟΥ ΔΕΙΣ ASSIGNMENT KAI costs)

from collections import deque
import sys , argparse

def GetPath(pred,v) :
    path = []
    while v != -1 :
        path.append(v)
        v = pred[v]
    return path

def IsPerfectMatching(matching) :
    perf = True
    for i in matching :
        if matching[i] == None :
            perf = False
            break
    return perf

def FindFirstUnmatched(matching,U) :
    for u in U :
        if matching[u] == None :
            return u

def ComputeDelta(g,oddes :
        for v in g[u] :
            if v not in odd_nodes :
                if  ASSIGNMENT :
                    c = costs[(u[0],v[1])] - prices[u] - prices[v]
                else :
                    if final :
                        c = costs[(u,v)][0] - prices[u] - prices[v]
                    else :
                        c = costs[(u,v)] - prices[u] - prices[v]
                if c < min :
                    min = c
    return min

def AugmentingPathBFS(g,node,matching,costs,prices,final) :
    q = deque()
    inqueue = {i: False for i in g}
    visited = {i: False for i in g}
    pred = {i: -1 for i in g}
    q.appendleft(node)
    inqueue[node] = True
    q.appendleft(-1)
    level = 0
    even_nodes = set()
    odd_nodes = set()
    while len(q) > 1 :
        c = q.pop()
        if c == -1 :
            level += 1
            c = q.pop()
            q.appendleft(-1)
        inqueue[c] = False
        visited[c] = True
        if level % 2 == 0 :
            next_level_odd = True
            even_nodes.add(c)
        else :
            next_level_odd = False
            odd_nodes.add(c)
        for v in g[c] :
            if not ASSIGNMENT :
                if final :
                    cost = costs[(c,v)][0]
                else :
                    cost = costs[(c,v)]
            else :
                if next_level_odd :
                    cost = costs[(c[0],v[1])]
                else :
                    cost = costs[(v[0],c[1])]
            if not visited[v] and cost == prices[c] + prices[v] :
                if next_level_odd and matching[v] == None :
                    pred[v] = c
                    augmenting_path = GetPath(pred,v)
                    return augmenting_path,odd_nodes,even_nodes  
                if ((next_level_odd and matching[c] != v) or (not next_level_odd and matching[c] == v)) and not inqueue[v] :
                    q.appendleft(v)
                    inqueue[v] = True
                    pred[v] = c
    return None,odd_nodes,even_nodes

def Hungarian(g,costs,final,U) :
    prices = {i: 0 for i in g}
    matching = {i: None for i in g}
    while not IsPerfectMatching(matching) :
        node = FindFirstUnmatched(matching,U)
        augmenting_path,odd_nodes,even_nodes = AugmentingPathBFS(g,node,matching,costs,prices,final)
        if augmenting_path != None :
            i = 0
            while i < len(augmenting_path) - 1 :
                matching[augmenting_path[i]] = augmenting_path[i + 1]
                matching[augmenting_path[i + 1]] = augmenting_path[i]
                i += 2
        else :
            delta = ComputeDelta(g,odd_nodes,even_nodes,costs,prices,final)
            for u in even_nodes :
                prices[u] += delta
            for v in odd_nodes :
                prices[v] -= delta
    return matching
