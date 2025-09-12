# Importar las clases de la base
from grafos import Accion
from grafos import Sala
from grafos import Nodo
from grafos import Problema


# Función principal del algoritmo, busca en todos los hijos de un nodo antes de pasar al siguiente
def profundidad(problema):
    raiz = crea_nodo_raiz(problema)
    if problema.es_objetivo(raiz.sala):
        return raiz
    frontera = [raiz,]
    explorados = set()
    while True:
        if not frontera:
            return None
        nodo = frontera.pop()
        explorados.add(nodo.sala)
        if not nodo.acciones:
            continue
        for nombre_accion in nodo.acciones.keys():
            accion = Accion(nombre_accion)
            hijo = crea_nodo_hijo(problema, nodo, accion)
            salas_frontera = [nodo.sala for nodo in frontera]
            if (hijo.sala not in explorados and hijo.sala not in salas_frontera):
                if problema.es_objetivo(hijo.sala):
                    return hijo
                frontera.append(hijo)


# Función que crea un nodo de inicio o la sala raíz, revisando si se encuentra entre las claves definidas
def crea_nodo_raiz(problema):
    sala_raiz = problema.sala_inicial
    acciones_raiz = {}
    if sala_raiz.nombre in problema.acciones.keys():
        acciones_raiz = problema.acciones[sala_raiz.nombre]
    raiz = Nodo(sala_raiz, None, acciones_raiz, None)
    return raiz


# Función que crea los nodos hijo de la sala en la que nos encontremos y los asigna al padre
def crea_nodo_hijo(problema, padre, accion):
    nueva_sala = problema.resultado(padre.sala, accion)
    acciones_nuevo = {}
    if nueva_sala.nombre in problema.acciones.keys():
        acciones_nuevo = problema.acciones[nueva_sala.nombre]
        hijo = Nodo(nueva_sala, accion, acciones_nuevo, padre)
        padre.hijos.append(hijo)
        return hijo
    

# Función para mostrar la solución, con el formato estructurado para mostrar la sala actual y la acción que se tomó para continuar. También imprime si la solución no existe
def muestra_solucion(objetivo=None):
    if not objetivo:
        print("No hay solución")
        return
    nodo = objetivo
    while nodo:
        msg = "Sala: {0}"
        print(msg.format(nodo.sala.nombre))
        if nodo.accion:
            msg = "<--- {0} ---"
            print(msg.format(nodo.accion.nombre))
        nodo = nodo.padre

# Declaraciones, comenzando con las acciones
if __name__ == '__main__':
    accN = Accion('adelante')
    accS = Accion('atras')
    accE = Accion('derecha')
    accO = Accion('izquierda')

# Declarar salas que existen con sus posibles acciones
    living = Sala('Sala', [accN, accE])
    corridor = Sala('Pasillo', [accN, accS, accO])
    bedroom = Sala('Cuarto', [accS])
    bathroom = Sala('Baño', [accE])
    kitchen = Sala('Cocina', [accO])

# Declarar qué movimientos llevan a qué salas
    movimientos = {'Sala': {'adelante': corridor,
                            'derecha': kitchen},
                   'Pasillo': {'adelante': bedroom,
                               'atras': living,
                               'izquierda': bathroom},
                   'Cuarto': {'atras': corridor},
                   'Baño': {'derecha': corridor},
                   'Cocina': {'izquierda': living}}
    
# Crear problemas para probar el algoritmo, por ejemplo moverse desde la recepción hasta la oficina
objetivo_1 = [bathroom]
problema_1 = Problema(living, objetivo_1, movimientos)

objetivo_2 = [kitchen]
problema_2 = Problema(bedroom, objetivo_2, movimientos)

objetivo_3 = [bedroom]
problema_3 = Problema(bathroom, objetivo_3, movimientos)

# Definir qué problema deseamos resolver
problema_resolver = problema_1

# Almacenar el resultado del algoritmo en una variable y mostrarla con nuestro formato
solucion = profundidad(problema_resolver)
muestra_solucion(solucion)