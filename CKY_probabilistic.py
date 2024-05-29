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

#######################################
########## CKY PROBABILISTIC ##########
#######################################

import sys

def parse_grammar_prob(grammar_text):
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
                llista_regles = []
                for regla in body.split():
                    if regla.isalpha():
                        # Si la regla és alfabètica i té més d’una lletra, afegiu cada símbol individualment
                        if len(regla) > 1:
                            llista_regles.extend(list(regla.strip()))
                        else:
                            llista_regles.append(regla.strip())
                    else:
                        # Si la regla conté un número (probabilitat), netegeu -la i afegiu -la juntament amb les regles
                        regla = regla.replace('(', '').replace(')', '')
                        grammar[head].append((llista_regles, float(regla)))



                    
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
            for value in rhs:
                if isinstance(value, list): # si no estem treballant amb la probabilitat
                    if len(value) == 1: # si trobem una regla unitària
                        if value[0] not in terminals:
                            print("Terminal no trobat:", value)
                            return False
                        
                    elif len(value) == 2: # si trobem una regla binària
                        if value[0] not in non_terminals or value[1] not in non_terminals:
                            print("No es troba el non_terminal:", value)
                            return False

                    elif len(value) >= 3: # si trobem una regla amb més de dos elements
                        return False
    
    return True


def CKY_prob(R, w):
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
            for value in rule:
                if isinstance(value, list):    
                    for symbol in value:
                        if symbol.isupper():
                            non_terminals.add(symbol)
                        elif symbol.islower():
                            terminals.add(symbol)

    #print("Non-terminals:", list(non_terminals))
    #print("Terminals:", list(terminals))
    
    gramatica_correcte = gramatica_CFN(non_terminals, terminals, R)

    if not gramatica_correcte:
        print('La gramàtica no està en forma norma de Chomsky')
        return
    
    T = {}           
    for j in range(1, n+1): # recorrem la paraula
        i = 1
        while j <= n:
            if i == j:
                # si la paraula té una sola lletra, busquem la regla que la conté
                val = [(key, regla[1]) for key, value in R.items() for regla in value if w[i-1] in regla[0]]                              
                T[(i, j)] = max(val, key=lambda x: x[1], default=[])
                
            else:
                val = []
                for k in range(i, j):
                    regla_A = T[(i, k)] # regles de la part esquerra
                    regla_B = T[(k+1, j)] # regles de la part dreta
                        
                    for key, value in R.items(): # recorrem totes les regles
                        for regla in value: # recorrem les regles
                            if regla_A and regla_B and [regla_A[0], regla_B[0]] == regla[0]: # si trobem una regla que contingui les dues parts
                                probabilitat = regla[1] * regla_A[1] * regla_B[1] # calculem la probabilitat
                                val.append((key, probabilitat)) 
                
                T[(i, j)] = max(val, key=lambda x: x[1], default=[]) # agafem la regla amb la probabilitat més alta
            
            i += 1
            j += 1
            
    if init_symbol in T[(1, n)]:
        print("La palabra '{}' es aceptada por la gramática.".format(w))
        return T
    else:
        print("La palabra '{}' no es aceptada por la gramática.".format(w))
        return T

# llegim la gramàtica del fitxer de text passada per paràmetre
def main():
    """Main function to read grammar and word from input files, and determine if the word is in the language."""
    if len(sys.argv) != 2:
        print("Usage: python CKY_probabilistic.py <grammar_file>")
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
                
    R = parse_grammar_prob(grammar_text)
    
    for string in strings.split('\n'):
        if string:
            print("Paraula a analitzar:", string)
            table = CKY_prob(R, string)
    
    while True:
        word = input("Introdueix la paraula a analitzar: ")
        
        table = CKY_prob(R, str(word))
        
        print("Taula:")
        for i in range(1, len(word)+1):
            for j in range(i, len(word)+1):
                print("T[{}, {}] = {}".format(i, j, table[(i, j)]))
                
        
        response = input("Vols continuar? (s/n): ")
        
        if response.lower() != 's':
            break

if __name__ == "__main__":
    main()