
from ast_nodes import (
    PaginaNode,
    TituloNode,
    EncabezadoNode,
    ParrafoNode,
    BotonNode
)


class SemanticError(Exception):
    pass


class SemanticAnalyzer:

    MAX_LONGITUD = 300

    def __init__(self, ast):
        self.ast = ast
        self.errores = []

    def analizar(self):

        # Comprobar que exista un documento valido
        if not isinstance(self.ast, PaginaNode):
            raise SemanticError(
                "SEM000: El documento no es una pagina valida."
            )

        titulos = 0
        encabezados = 0

        # Recorrer todos los nodos del AST
        for instruccion in self.ast.instrucciones:

            # Comprobar el tipo de instruccion
            if isinstance(instruccion, TituloNode):
                titulos += 1

            elif isinstance(instruccion, EncabezadoNode):
                encabezados += 1

            elif not isinstance(
                instruccion,
                (ParrafoNode, BotonNode)
            ):
                self.errores.append(
                    "SEM006: Se encontro un nodo desconocido."
                )
                continue

            # Obtener el texto de la instruccion
            texto = instruccion.texto

            # Regla: el texto no puede estar vacio
            if not texto.strip():
                self.errores.append(
                    "SEM003: Una instruccion contiene texto vacio."
                )

            # Regla: longitud maxima
            if len(texto) > self.MAX_LONGITUD:
                self.errores.append(
                    "SEM005: Un texto supera los 300 caracteres."
                )

        # Regla: debe existir un titulo
        if titulos == 0:
            self.errores.append(
                "SEM001: La pagina debe tener un titulo."
            )

        # Regla: solamente puede existir un titulo
        if titulos > 1:
            self.errores.append(
                "SEM002: La pagina solo permite un titulo."
            )

        # Regla: debe existir al menos un encabezado
        if encabezados == 0:
            self.errores.append(
                "SEM004: La pagina debe tener un encabezado."
            )

        # Mostrar los errores encontrados
        if self.errores:

            mensaje = "\n".join(self.errores)

            raise SemanticError(mensaje)

        return True
