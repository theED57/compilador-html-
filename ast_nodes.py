
# Nodo principal del programa
class PaginaNode:

    def __init__(self, instrucciones):
        self.instrucciones = instrucciones


# Nodo para el titulo de la pagina
class TituloNode:

    def __init__(self, texto):
        self.texto = texto


# Nodo para el encabezado
class EncabezadoNode:

    def __init__(self, texto):
        self.texto = texto


# Nodo para los parrafos
class ParrafoNode:

    def __init__(self, texto):
        self.texto = texto


# Nodo para los botones
class BotonNode:

    def __init__(self, texto):
        self.texto = texto
