
import json

from ast_nodes import (
    PaginaNode,
    TituloNode,
    EncabezadoNode,
    ParrafoNode,
    BotonNode
)


class IntermediateError(Exception):
    pass


# Representa una instruccion del codigo intermedio
class IRInstruction:

    def __init__(self, operacion, valor=None):
        self.operacion = operacion
        self.valor = valor

    def __str__(self):

        if self.valor is None:
            return self.operacion

        texto = json.dumps(
            self.valor,
            ensure_ascii=False
        )

        return f"{self.operacion} {texto}"


# Generador de codigo intermedio
class IntermediateGenerator:

    def __init__(self, ast):
        self.ast = ast
        self.instrucciones = []

    # Agregar una instruccion al codigo intermedio
    def agregar(self, operacion, valor=None):

        instruccion = IRInstruction(operacion, valor)

        self.instrucciones.append(instruccion)

    # Recorrer el AST y generar el codigo intermedio
    def generar(self):

        if not isinstance(self.ast, PaginaNode):
            raise IntermediateError(
                "El AST no representa una pagina valida."
            )

        self.instrucciones = []

        # Inicio de la pagina
        self.agregar("CREATE_PAGE")

        # Recorrer las instrucciones del AST
        for nodo in self.ast.instrucciones:

            if isinstance(nodo, TituloNode):

                self.agregar(
                    "SET_TITLE",
                    nodo.texto
                )

            elif isinstance(nodo, EncabezadoNode):

                self.agregar(
                    "ADD_HEADING",
                    nodo.texto
                )

            elif isinstance(nodo, ParrafoNode):

                self.agregar(
                    "ADD_PARAGRAPH",
                    nodo.texto
                )

            elif isinstance(nodo, BotonNode):

                self.agregar(
                    "ADD_BUTTON",
                    nodo.texto
                )

            else:

                raise IntermediateError(
                    f"Nodo no reconocido: {type(nodo).__name__}"
                )

        # Finalizar la pagina
        self.agregar("END_PAGE")

        return self.instrucciones
