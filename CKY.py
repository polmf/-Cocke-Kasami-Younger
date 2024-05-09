# lectura de Gramatica en Forma Normal de Chomsky y algoritmo CYK

non_terminals = ["NP", "Nom", "Det", "AP", 
                  "Adv", "A"]
terminals = ["book", "orange", "man", 
             "tall", "heavy", 
             "very", "muscular"]
 
# Rules of the grammar
R = {
     "S": [['a'], ['X', 'A'], ['A', 'X'], ['b']],
     "A": [['R', 'B']],
     "B": [['A', 'X'], ['b'], ['a']],
     "X": [['a']],
     "R": [['X', 'B']]
    }

init_symbol = 'S'


def CKY(non_terminals, terminals, R, init_symbol, w):
    n = len(w)
    
    # fer una taula nxn
    T = [[set([]) for j in range(n)] for i in range(n)]
    print(T)
    
    
    
    
    T = [[set([]) for j in range(n)] for i in range(n)]
    for j in range(0, n):
        for lhs, rule in R.items():
            for rhs in rule:
                if len(rhs) == 1 and rhs[0] == w[j]:
                    T[j][j].add(lhs)
        for i in range(j, -1, -1): 
            for k in range(i, j + 1):	 
                for lhs, rule in R.items():
                    for rhs in rule:
                        if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                            T[i][j].add(lhs)
    return T