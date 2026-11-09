
from ast_nodes import (
    PaginaNode,
    TituloNode,
    EncabezadoNode,
    ParrafoNode,
    BotonNode
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    # Obtener el token actual
    def actual(self):
        return self.tokens[self.posicion]

    # Comprobar si el token tiene el tipo esperado
    def esperar(self, tipo):

        token = self.actual()

        if token.tipo == tipo:
            self.posicion += 1
            return token

        raise SyntaxError(
            f"Se esperaba {tipo}, pero se encontro "
            f"{token.tipo} en linea {token.linea}, "
            f"columna {token.columna}"
        )

    # Comprobar una palabra reservada
    def esperar_palabra(self, palabra):

        token = self.actual()

        if (
            token.tipo == "PALABRA_CLAVE"
            and token.valor == palabra
        ):
            self.posicion += 1
            return token

        raise SyntaxError(
            f"Se esperaba '{palabra}' en linea "
            f"{token.linea}, columna {token.columna}"
        )

    # Analizar una instruccion individual
    def analizar_instruccion(self):

        token = self.actual()

        if token.tipo != "PALABRA_CLAVE":
            raise SyntaxError(
                f"Instruccion no valida en linea {token.linea}"
            )

        palabra = token.valor

        self.posicion += 1

        # Todas las instrucciones necesitan un texto
        texto = self.esperar("TEXTO").valor

        if palabra == "titulo":
            return TituloNode(texto)

        elif palabra == "encabezado":
            return EncabezadoNode(texto)

        elif palabra == "parrafo":
            return ParrafoNode(texto)

        elif palabra == "boton":
            return BotonNode(texto)

    # Analizar el documento completo
    def analizar(self):

        self.esperar_palabra("pagina")

        self.esperar("ABRE_LLAVE")

        instrucciones = []

        # Analizar instrucciones hasta encontrar }
        while self.actual().tipo != "CIERRA_LLAVE":

            if self.actual().tipo == "EOF":
                token = self.actual()

                raise SyntaxError(
                    f"Falta cerrar la pagina. "
                    f"Fin inesperado en linea {token.linea}"
                )

            instruccion = self.analizar_instruccion()

            instrucciones.append(instruccion)

        self.esperar("CIERRA_LLAVE")

        # No permitir contenido despues de la pagina
        self.esperar("EOF")

        return PaginaNode(instrucciones)
