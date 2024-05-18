import random
import string

def to_fnc(rules):
    new_rules = dict(rules)
    new_non_terms = set()
    for key in rules.keys():
        new_non_terms.add(key)
        
    print(new_non_terms)
    # Función para obtener un nuevo símbolo no terminal
    def get_new_non_term():
        nonlocal new_non_terms
        available_non_terms = set(string.ascii_uppercase) - new_non_terms
        if not available_non_terms:
            # Si no hay letras no terminales disponibles, agrega nuevas letras al conjunto
            new_non_terms = set()
            available_non_terms = set(string.ascii_uppercase)
        new_non_term = random.choice(list(available_non_terms))
        new_non_terms.add(new_non_term)
        return new_non_term

    # Identificar producciones que no están en FNC
    to_replace = []
    for key, value in rules.items():
        if len(value) > 1 or (len(value) == 1 and len(value[0]) > 2):
            to_replace.append(key)

    # Reemplazar producciones no FNC
    for key in to_replace:
        value = new_rules.pop(key)
        new_key = get_new_non_term()
        new_rules[key] = [[value[0][0], new_key]]
        new_rules[new_key] = [value[0][1:]]

    return new_rules


# Reglas originales
rules = {
    "S": [['A', 'B', 'C']],
    "F": [['B', 'Q', 'A']],
    "A": [['a',]],
    "B": [['b']],
    "C": [['c']],
    "Q": [['q']]
}

# Convertir a FNC
fnc_rules = to_fnc(rules)

# Mostrar las reglas en FNC
print(fnc_rules)
