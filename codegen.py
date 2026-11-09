
from html import escape
from pathlib import Path

from intermediate import IRInstruction


class CodeGenerationError(Exception):
    pass


class CodeGenerator:

    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.html = []

    def generar(self):

        self.html = []

        # Comprobar que exista el inicio del documento
        if not self.instrucciones:
            raise CodeGenerationError(
                "No existen instrucciones intermedias."
            )

        if self.instrucciones[0].operacion != "CREATE_PAGE":
            raise CodeGenerationError(
                "El codigo intermedio debe comenzar con CREATE_PAGE."
            )

        if self.instrucciones[-1].operacion != "END_PAGE":
            raise CodeGenerationError(
                "El codigo intermedio debe terminar con END_PAGE."
            )

        # Estructura inicial del documento HTML
        self.html.extend([
            "<!DOCTYPE html>",
            '<html lang="es">',
            "<head>",
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        ])

        pagina_iniciada = False
        pagina_finalizada = False

        for instruccion in self.instrucciones:

            operacion = instruccion.operacion
            valor = instruccion.valor

            if pagina_finalizada:
                raise CodeGenerationError(
                    "No puede haber instrucciones despues de END_PAGE."
                )

            if operacion == "CREATE_PAGE":

                if pagina_iniciada:
                    raise CodeGenerationError(
                        "CREATE_PAGE no puede repetirse."
                    )

                if valor is not None:
                    raise CodeGenerationError(
                        "CREATE_PAGE no debe tener un valor."
                    )

                pagina_iniciada = True

            elif operacion == "SET_TITLE":

                if not pagina_iniciada:
                    raise CodeGenerationError(
                        "SET_TITLE debe aparecer dentro de la pagina."
                    )

                if valor is None:
                    raise CodeGenerationError(
                        "SET_TITLE necesita un texto."
                    )

                titulo = escape(str(valor), quote=True)

                self.html.append(
                    f"    <title>{titulo}</title>"
                )

            elif operacion == "ADD_HEADING":

                if not pagina_iniciada or valor is None:
                    raise CodeGenerationError(
                        "ADD_HEADING necesita una pagina y un texto."
                    )

                texto = escape(str(valor), quote=True)

                self.html.append("</head>")
                self.html.append("<body>")
                self.html.append(f"    <h1>{texto}</h1>")

            elif operacion == "ADD_PARAGRAPH":

                if not pagina_iniciada or valor is None:
                    raise CodeGenerationError(
                        "ADD_PARAGRAPH necesita una pagina y un texto."
                    )

                texto = escape(str(valor), quote=True)

                self.html.append(
                    f"    <p>{texto}</p>"
                )

            elif operacion == "ADD_BUTTON":

                if not pagina_iniciada or valor is None:
                    raise CodeGenerationError(
                        "ADD_BUTTON necesita una pagina y un texto."
                    )

                texto = escape(str(valor), quote=True)

                self.html.append(
                    f"    <button>{texto}</button>"
                )

            elif operacion == "END_PAGE":

                if not pagina_iniciada:
                    raise CodeGenerationError(
                        "No se puede finalizar una pagina sin iniciarla."
                    )

                if valor is not None:
                    raise CodeGenerationError(
                        "END_PAGE no debe tener un valor."
                    )

                # Si no hubo encabezado, cerrar head y abrir body
                if "</head>" not in self.html:
                    self.html.append("</head>")
                    self.html.append("<body>")

                self.html.append("</body>")
                self.html.append("</html>")

                pagina_finalizada = True

            else:

                raise CodeGenerationError(
                    f"Instruccion IR desconocida: {operacion}"
                )

        if not pagina_finalizada:
            raise CodeGenerationError(
                "El documento HTML no pudo finalizarse."
            )

        return "\n".join(self.html)

    # Guardar el HTML generado en un archivo
    def guardar(self, ruta="output/salida.html"):

        contenido = self.generar()

        archivo = Path(ruta)

        # Crear la carpeta si no existe
        archivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Guardar el documento
        archivo.write_text(
            contenido,
            encoding="utf-8"
        )

        return archivo
