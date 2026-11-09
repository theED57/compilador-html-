
class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"{self.tipo}: {self.valor}"


class Lexer:

    PALABRAS_RESERVADAS = [
        "pagina",
        "titulo",
        "encabezado",
        "parrafo",
        "boton"
    ]

    def __init__(self, codigo):
        self.codigo = codigo
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []

    def avanzar(self):
        caracter = self.codigo[self.posicion]

        if caracter == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1

        self.posicion += 1

    def analizar(self):

        while self.posicion < len(self.codigo):

            caracter = self.codigo[self.posicion]

            # Ignorar espacios y saltos de linea
            if caracter.isspace():
                self.avanzar()
                continue

            linea = self.linea
            columna = self.columna

            # Reconocer llaves
            if caracter == "{":
                self.tokens.append(
                    Token("ABRE_LLAVE", "{", linea, columna)
                )
                self.avanzar()
                continue

            if caracter == "}":
                self.tokens.append(
                    Token("CIERRA_LLAVE", "}", linea, columna)
                )
                self.avanzar()
                continue

            # Reconocer textos entre comillas
            if caracter == '"':
                self.avanzar()
                texto = ""

                while (
                    self.posicion < len(self.codigo)
                    and self.codigo[self.posicion] != '"'
                ):
                    if self.codigo[self.posicion] == "\n":
                        raise SyntaxError(
                            f"Texto sin cerrar en linea {linea}"
                        )

                    if self.codigo[self.posicion] == "\\":
                        self.avanzar()

                        if self.posicion >= len(self.codigo):
                            raise SyntaxError("Escape incompleto")

                        siguiente = self.codigo[self.posicion]

                        if siguiente not in ['"', '\\']:
                            raise SyntaxError(
                                f"Escape no valido en linea {self.linea}"
                            )

                        texto += siguiente
                        self.avanzar()
                        continue

                    texto += self.codigo[self.posicion]
                    self.avanzar()

                if self.posicion >= len(self.codigo):
                    raise SyntaxError(
                        f"Texto sin cerrar en linea {linea}"
                    )

                self.avanzar()

                self.tokens.append(
                    Token("TEXTO", texto, linea, columna)
                )
                continue

            # Reconocer palabras
            if caracter.isalpha() or caracter == "_":

                palabra = ""

                while self.posicion < len(self.codigo):

                    actual = self.codigo[self.posicion]

                    if actual.isalnum() or actual == "_":
                        palabra += actual
                        self.avanzar()
                    else:
                        break

                if palabra in self.PALABRAS_RESERVADAS:
                    self.tokens.append(
                        Token("PALABRA_CLAVE", palabra, linea, columna)
                    )
                else:
                    raise SyntaxError(
                        f"Palabra desconocida '{palabra}' "
                        f"en linea {linea}, columna {columna}"
                    )

                continue

            # Cualquier otro caracter es invalido
            raise SyntaxError(
                f"Caracter inesperado '{caracter}' "
                f"en linea {linea}, columna {columna}"
            )

        self.tokens.append(
            Token("EOF", "FIN", self.linea, self.columna)
        )

        return self.tokens
