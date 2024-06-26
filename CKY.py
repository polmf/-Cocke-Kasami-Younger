# lectura de Gramatica en Forma Normal de Chomsky y algoritmo CYK

"""
Context Free Grammar: 
We are given a Context Free Grammar G = (V, X, R, S) and a string w, where:

V is a finite set of variables or non-terminal symbols,
X is a finite set of terminal symbols,
R is a finite set of rules,
S is the start symbol, a distinct element of V, and
V and X are assumed to be disjoint sets.
"""

import sys

def parse_grammar(grammar_text):
    """Analitzem la gramàtica d’un text determinat.
    
    Args:
        grammar_text (str): Regles de gramàtica a CNF, una per línia.
        
    Returns:
        dict: Representació del diccionari de la gramàtica.
    """
    grammar = {}
    for line in grammar_text.strip().split('\n'):
        if '->' in line:
            head, bodies = line.split('->')
            head = head.strip()
            bodies = bodies.strip().split('|')
            
            if head not in grammar:
                grammar[head] = []
            
            for body in bodies:
                if len(body) > 1:
                    llista_bodies = [regla for regla in body.strip()]
                    grammar[head].append(llista_bodies)
                else:
                    grammar[head].append(body.strip().split())
                    
    return grammar


def gramatica_CFN(non_terminals, terminals, R):
    """
    Recorre totes les regles i comprova que les unitàries siguin terminals i les binàries no terminals.
    A més, assegura que les regles només siguin unitàries o binàries.
    
    Parameters:
        non_terminals (set): Conjunt de no terminals
        terminals (set): Conjunt de terminals
        R (dict): Diccionari de la gramàtica
        
    Returns:
        bool: Retorna True si la gramàtica és correcta, False si no ho és
    """
    
    for lhs, rule in R.items():
        for rhs in rule:
            if len(rhs) == 1: # si trobem una regla unitària
                if rhs[0] not in terminals:
                    print('La regla unitària', rhs[0], 'no és terminal')
                    print('Terminals:', terminals)
                    return False
                
            if len(rhs) == 2: # si trobem una regla binària
                if rhs[0] not in non_terminals or rhs[1] not in non_terminals:
                    print('La regla binària', rhs, 'no és no terminal')
                    print('No terminals:', non_terminals)
                    return False

            if len(rhs) >= 3: # si trobem una regla amb més de dos elements
                print('La regla', rhs, 'té més de dos elements')
                return False
    
    return True


def CKY(R, w):
    """
    Aquesta funció implementa l'algoritme CKY per determinar si una paraula w pertany al llenguatge generat per una gramàtica G.
    
    Rep com a paràmetres:
    - R: un diccionari que representa la gramàtica en Forma Normal de Chomsky.
    - w: una paraula que volem analitzar.
    
    Retorna:
    - T: una taula que conté les regles de producció que s'han aplicat per generar la paraula w.
    """
    
    n = len(w)
    
    init_symbol = next(iter(R))
    non_terminals = set()
    terminals = set()
    non_terminals.add(init_symbol)

    # Recorrem tota la gramàtica per trobar els no terminals i terminals
    for rules in R.values():
        for rule in rules:
            for symbol in rule:
                if str(symbol) == 'ε' or str(symbol) == 'Ɛ' or symbol.islower():
                    terminals.add(symbol)
                else:
                    non_terminals.add(symbol)
    
    gramatica_correcte = gramatica_CFN(non_terminals, terminals, R)

    if not gramatica_correcte:
        print('La gramàtica no està en forma norma de Chomsky\n')
        return
    
    
    def pot_generar_buida(R, symbol):
        
        for regla in R[symbol]:
            if len(regla) == 2:
                if pot_generar_buida(R, regla[0]) and pot_generar_buida(R, regla[1]):
                    return True
            else:
                if regla == ['ε'] or regla == ['Ɛ']:return True
        
        return False

    
    if w == "":
        if pot_generar_buida(R, init_symbol):
            print("La paraula buida és acceptada per la gramàtica.\n")
            return {}
        else:
            print("La paraula buida no és acceptada per la gramàtica.\n")
            return {}
    
    
    T = {}           
    for j in range(1, n+1): # recorrem la paraula
        i = 1
        while j <= n: 
            if i == j: 
                # si la paraula té una sola lletra, busquem la regla que la conté
                T[(i, j)] = [key for key, value in R.items() if [w[i-1]] in value]                    
                
            else:
                val = []
                for k in range(i, j): 
                    regla_A = T[(i, k)] # regles de la part esquerra
                    regla_B = T[(k+1, j)] # regles de la part dreta
                    
                    for key, value in R.items(): # recorrem totes les regles de la gramàtica
                        for rule in value:
                            if len(rule) == 2 and rule[0] in regla_A and rule[1] in regla_B: # si la regla té dos parts i trobem una regla que contingui les dues parts
                                val.append(key)
                            
                T[(i, j)] = val # afegim les regles que hem trobat
                
            i += 1
            j += 1
            
    if init_symbol in T[(1, n)]:
        print("La paraula '{}' es acceptada per la gramàtica.\n".format(w))
        return T
    else:
        print("La paraula '{}' no es acceptada por la gramàtica.\n".format(w))
        return T


# llegim la gramàtica del fitxer de text passada per paràmetre
def main():
    """Funció principal per llegir fitxers d’entrada de gramàtica i paraules i determinar si la paraula es troba en l’idioma."""
    
    if len(sys.argv) != 2:
        print("Us: python CKY.py <grammar_file>")
        sys.exit(1)
    
    grammar_file = sys.argv[1]
    
    # Llegim la gramàtica del fitxer de text
    with open(grammar_file, 'r', encoding='utf-8') as f:
        grammar_text, strings = "", ""
        for line in f.readlines():
            if len(line.split()) > 1:
                grammar_text += line
            else:
                strings += line
                
    R = parse_grammar(grammar_text)
    
    for string in strings.split('\n'):
        print("Paraula a analitzar:", string)
        table = CKY(R, string)
    
    while True:
        
        word = input("Introdueix la paraula a analitzar: ")
        
        table = CKY(R, word)
        
        response = input("Vols continuar? (s/n): ")
        
        if response.lower() != 's':
            break

if __name__ == "__main__":
    main()    