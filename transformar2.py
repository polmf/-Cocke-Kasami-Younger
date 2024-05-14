def remove_unit_rules(rules):
    # Diccionario para almacenar las reglas sin reglas unitarias
    new_rules = {}

    # Diccionario para almacenar las reglas unitarias que convierten un símbolo no terminal en otro símbolo no terminal
    unit_rules = {}

    # Recorremos todas las reglas
    for key, value in rules.items():
        # Si la regla tiene solo un símbolo no terminal en el lado derecho
        if len(value) == 1 and len(value[0]) == 1 and value[0][0] in rules and value[0][0] != key:
            # Verificamos si el símbolo es no terminal o terminal
            if value[0][0] in new_rules:
                # Agregamos la regla unitaria al diccionario de reglas unitarias
                unit_rules[key] = value[0][0]
            else:
                # Agregamos la regla al diccionario de reglas sin reglas unitarias
                new_rules[key] = value
        else:
            # Agregamos la regla al diccionario de reglas sin reglas unitarias
            new_rules[key] = value

    # Procesamos las reglas unitarias
    for unit_key, unit_value in unit_rules.items():
        # Obtenemos todas las producciones de la regla unitaria
        unit_productions = rules[unit_value]
        # Agregamos las producciones de la regla unitaria al conjunto de reglas sin reglas unitarias
        new_rules[unit_key] = unit_productions

    return new_rules

# Reglas originales
rules = {
    "S": [['A', 'B']],
    "Z": [['C'], ['z']],
    "A": [['a',]],
    "B": [['b']],
    "C": [['c'], ['d'], ['e']],
}

# Eliminamos reglas unitarias
new_rules = remove_unit_rules(rules)

# Mostramos las nuevas reglas
print(new_rules)
