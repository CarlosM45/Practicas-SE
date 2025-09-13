# Modus Tollens es una regla de inferencia que sigue la lógica "Si P, entonces Q" pero en la que se niega el consecuente, para probar que no cumple con el antecedente
# Es decir: "Q no es verdadero, así que P no es verdadero"
# Por ejemplo: "Si un objeto está hecho de hierro, será atraído al imán. Este objeto no es atraído por el imán, así que no es de hierro"

def modus_tollens(P, Q):
    if not Q:
        print("P es falso")
    else:
        print("No se puede aplicar Modus Tollens porque Q es verdadero")


P = True
Q = False
modus_tollens(P, Q)
