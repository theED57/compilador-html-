from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer, SemanticError
from intermediate import IntermediateGenerator, IntermediateError
from codegen import CodeGenerator, CodeGenerationError


# LEER EL ARCHIVO 
from pathlib import Path

ruta_entrada = Path("ejemplos/ejemplo.mw")

codigo = ruta_entrada.read_text(encoding="utf-8")


try:

    # FASE 1: ANALISIS LEXICO
    print("=== ANALISIS LEXICO ===\n")

    lexer = Lexer(codigo)
    tokens = lexer.analizar()
    from semantic import SemanticAnalyzer


    for token in tokens:
        print(token)


    # FASE 2: ANALISIS SINTACTICO
    print("\n=== ANALISIS SINTACTICO ===\n")

    parser = Parser(tokens)
    ast = parser.analizar()

    print("Sintaxis correcta.")
    print("AST generado correctamente.")

    # FASE 3: ANALISIS SEMANTICO
    print("\n=== ANALISIS SEMANTICO ===\n")
    semantic = SemanticAnalyzer(ast)
    semantic.analizar()

    print("Analisis semantico correcto")
    print("El documento cumple con todas las reglas semanticas.")

    # FASE 4: GENERACION DE CODIGO INTERMEDIO
    print("\n=== GENERACION DE CODIGO INTERMEDIO ===\n")

    generador = IntermediateGenerator(ast)
    codigo_intermedio = generador.generar()

    for intruccion in codigo_intermedio:
        print(intruccion)
    
    print("\nCodigo intermedio generado correctamente.")

    # FASE 5: GENERACION DE CODIGO HTML
    print("\n=== GENERACION DE CODIGO HTML ===\n")

    generador_html = CodeGenerator(codigo_intermedio)
    ruta_salida = Path("output/salida.html")

    archivo_generado = generador_html.guardar(ruta_salida)
    print("Codigo HTML generado correctamente.")
    print(f"Archivo generado en: {archivo_generado}")


    # MOSTRAR EL AST
    print("\n=== ARBOL AST ===\n")

    print("PaginaNode")

    for instruccion in ast.instrucciones:

        if hasattr(instruccion, "texto"):

            nombre = type(instruccion).__name__

            print(f"  └── {nombre}: {instruccion.texto}")



except SyntaxError as error:
    print("\nERROR DEL COMPILADOR:")
    print(error)

except SemanticError as error:
    print("\nERROR SEMANTICO:")
    print(error)

except SyntaxError as error:
    print("\nERROR SINTACTICO:")
    print(error)

except IntermediateError as error:
    print("\nERROR EN CODIGO INTERMEDIO:")
    print(error)

except CodeGenerationError as error:
    print("\nERROR EN GENERACION HTML:")
    print(error)