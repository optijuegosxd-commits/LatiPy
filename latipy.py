#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LatiPy v0.2: prototipo educativo en espanol latino sin tildes en comandos.

No es un entorno aislado (sandbox): el codigo LatiPy puede acceder a Python y al sistema.
Usa solo la biblioteca estandar de Python 3.10+.
"""
from __future__ import annotations

import argparse
import builtins
import difflib
import io
import random
import re
import sys
import tokenize
from pathlib import Path
from typing import Iterable

VERSION = "0.2.0"

# Solo se traducen tokens de nombre. Las cadenas, los comentarios y los nombres
# de variables no se reemplazan a ciegas.
TOKEN_TRANSLATIONS = {
    "Falso": "False", "Nada": "None", "Verdadero": "True",
    "y": "and", "como": "as", "verificar": "assert", "asincrono": "async", "esperar": "await",
    "romper": "break", "caso": "case", "clase": "class", "continuar": "continue", "funcion": "def",
    "borrar": "del", "sino_si": "elif", "si_no": "else", "capturar": "except", "siempre": "finally",
    "para": "for", "desde": "from", "si": "if", "importar": "import", "en": "in",
    "es_mismo_objeto": "is", "funcion_anonima": "lambda", "ambito_externo": "nonlocal", "no": "not",
    "o": "or", "sin_operacion": "pass", "lanzar": "raise", "devolver": "return", "intentar": "try",
    "elegir": "match", "mientras": "while", "con": "with", "ceder": "yield",
}

BUILTIN_ALIASES = {
    "absoluto": "abs", "iterador_asincrono": "aiter", "todos": "all", "siguiente_asincrono": "anext",
    "alguno": "any", "representar_ascii": "ascii", "a_binario": "bin", "logico": "bool",
    "punto_de_pausa": "breakpoint", "arreglo_bytes": "bytearray", "octetos": "bytes",
    "es_invocable": "callable", "caracter": "chr", "metodo_de_clase": "classmethod", "compilar": "compile",
    "complejo": "complex", "derechos_de_autor": "copyright", "creditos": "credits", "borrar_atributo": "delattr",
    "diccionario": "dict", "listar_atributos": "dir", "division_y_resto": "divmod", "enumerar": "enumerate",
    "evaluar": "eval", "ejecutar_codigo": "exec", "salir": "exit", "filtrar": "filter", "decimal": "float",
    "formatear": "format", "conjunto_fijo": "frozenset", "obtener_atributo": "getattr", "globales": "globals",
    "tiene_atributo": "hasattr", "huella": "hash", "ayuda": "help", "a_hexadecimal": "hex", "identidad": "id",
    "preguntar": "input", "entero": "int", "es_instancia": "isinstance", "es_subclase": "issubclass",
    "crear_iterador": "iter", "longitud": "len", "licencia": "license", "lista": "list", "locales": "locals",
    "transformar": "map", "maximo": "max", "vista_memoria": "memoryview", "minimo": "min", "siguiente": "next",
    "objeto": "object", "a_octal": "oct", "abrir": "open", "codigo_de_caracter": "ord", "potencia": "pow",
    "mostrar": "print", "propiedad": "property", "terminar": "quit", "rango": "range", "representacion": "repr",
    "invertir": "reversed", "redondear": "round", "conjunto": "set", "fijar_atributo": "setattr", "segmento": "slice",
    "ordenar": "sorted", "metodo_estatico": "staticmethod", "texto": "str", "sumar": "sum", "super_clase": "super",
    "tupla": "tuple", "tipo": "type", "variables": "vars",
}

EXTRA_VALUES = {"PuntosSuspensivos": Ellipsis, "NoImplementado": NotImplemented}

# Ayudas pequenas pensadas para ejemplos y programas introductorios.
def preguntar_numero(mensaje="Escribe un numero entero: "):
    while True:
        respuesta = input(mensaje)
        try:
            return int(respuesta)
        except ValueError:
            print("Eso no parece un entero. Prueba otra vez.")


def preguntar_decimal(mensaje="Escribe un numero decimal: "):
    while True:
        respuesta = input(mensaje)
        try:
            return float(respuesta.replace(",", "."))
        except ValueError:
            print("Eso no parece un decimal. Prueba otra vez.")


def numero_aleatorio(minimo, maximo):
    """Devuelve un entero aleatorio entre minimo y maximo, ambos incluidos."""
    return random.randint(minimo, maximo)


def elegir_al_azar(elementos):
    """Devuelve un elemento aleatorio de una secuencia no vacia."""
    return random.choice(elementos)


def _quitar_comentario(linea: str) -> str:
    """Devuelve la parte de codigo, sin un comentario # fuera de cadenas."""
    i = 0
    quote = None
    triple = False
    escaped = False
    while i < len(linea):
        ch = linea[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif triple and linea.startswith(quote * 3, i):
                quote = None
                triple = False
                i += 2
            elif not triple and ch == quote:
                quote = None
        else:
            if ch == "#":
                return linea[:i]
            if ch in ("'", '"'):
                quote = ch
                triple = linea.startswith(ch * 3, i)
                if triple:
                    i += 2
        i += 1
    return linea


BLOCK_OPENERS = ("si", "sino_si", "mientras", "para", "funcion", "clase", "intentar", "con", "elegir")
BLOCK_BRANCHES = ("sino_si", "si_no", "capturar", "siempre", "caso")


def _parece_apertura_sin_dos_puntos(linea: str) -> bool:
    codigo = _quitar_comentario(linea).strip()
    if not codigo:
        return False
    primero = codigo.split(None, 1)[0].rstrip(":")
    return primero in BLOCK_OPENERS and not codigo.endswith(":")


def _primer_token_por_linea(codigo: str) -> dict[int, str]:
    """Obtiene el primer token real de cada linea (ignora textos y comentarios)."""
    primeros: dict[int, str] = {}
    ignorar = {tokenize.ENCODING, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
               tokenize.DEDENT, tokenize.COMMENT, tokenize.ENDMARKER}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(codigo).readline):
            if tok.type in ignorar:
                continue
            fila, columna = tok.start
            if fila not in primeros:
                primeros[fila] = tok.string if tok.type == tokenize.NAME else "<otro>"
    except (tokenize.TokenError, IndentationError):
        # La compilacion posterior mostrara el error real. Los tokens parciales
        # alcanzan para reconocer el modo facil sin leer palabras dentro de strings.
        pass
    return primeros


def _filas_internas_cadenas(codigo: str) -> set[int]:
    """Filas ocupadas por el interior de una cadena triple de varias lineas."""
    internas: set[int] = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(codigo).readline):
            if tok.type == tokenize.STRING and tok.end[0] > tok.start[0]:
                internas.update(range(tok.start[0] + 1, tok.end[0] + 1))
    except (tokenize.TokenError, IndentationError):
        pass
    return internas


def _normalizar_bloques_faciles(codigo: str) -> str:
    """Permite bloques con fin y sin dos puntos ni indentacion obligatoria.

    Ejemplo:
        si edad >= 18
            mostrar("Mayor")
        si_no
            mostrar("Menor")
        fin

    La forma clasica con dos puntos e indentacion sigue funcionando si no se usa fin.
    Un solo fin cierra un bloque elegir/caso completo.
    """
    lineas = codigo.splitlines()
    primeros = _primer_token_por_linea(codigo)
    filas_cadena = _filas_internas_cadenas(codigo)
    filas_fin = {
        fila for fila, token in primeros.items()
        if token == "fin" and re.fullmatch(r"\s*fin\s*(?:#.*)?", lineas[fila - 1])
    }
    filas_apertura_sin_dos_puntos = set()
    for fila, token in primeros.items():
        if token in BLOCK_OPENERS:
            sin_comentario = _quitar_comentario(lineas[fila - 1]).rstrip()
            if sin_comentario and not sin_comentario.endswith(":"):
                filas_apertura_sin_dos_puntos.add(fila)
    modo_facil = bool(filas_fin or filas_apertura_sin_dos_puntos)
    if not modo_facil:
        return codigo

    salida: list[str] = []
    pila: list[str] = []
    profundidad = 0
    for num, original in enumerate(lineas, start=1):
        # El interior de cadenas multilínea es contenido literal, no instrucciones.
        if num in filas_cadena:
            salida.append(original)
            continue
        contenido = original.strip()
        if not contenido:
            salida.append("")
            continue
        if contenido.startswith("#"):
            salida.append("    " * profundidad + contenido)
            continue
        token_primero = primeros.get(num)
        codigo_sin_comentario = _quitar_comentario(contenido).strip()
        if num in filas_fin and re.fullmatch(r"fin\s*", codigo_sin_comentario):
            if not pila:
                raise LatiPySourceError(f"Linea {num}: aparece 'fin' sin un bloque abierto.")
            if pila[-1] == "caso" and len(pila) >= 2 and pila[-2] == "elegir":
                pila.pop()  # caso
                pila.pop()  # elegir: un fin cierra la seleccion completa
                profundidad -= 2
            else:
                pila.pop()
                profundidad -= 1
            continue

        primer_token = token_primero if token_primero not in (None, "<otro>") else ""
        if primer_token == "caso":
            if pila and pila[-1] == "caso":
                pila.pop()
                profundidad -= 1
            if not pila or pila[-1] != "elegir":
                raise LatiPySourceError(f"Linea {num}: 'caso' debe estar dentro de un bloque 'elegir'.")
        elif primer_token in BLOCK_BRANCHES:
            if profundidad <= 0 or not pila:
                raise LatiPySourceError(f"Linea {num}: '{primer_token}' necesita un bloque anterior abierto.")
            pila.pop()
            profundidad -= 1

        # En el modo facil la sangria la administra LatiPy. Aceptamos dos puntos
        # opcionales al final de una apertura o rama.
        if primer_token in BLOCK_OPENERS + BLOCK_BRANCHES:
            codigo_parte = _quitar_comentario(contenido).rstrip()
            comentario = contenido[len(_quitar_comentario(contenido)):]
            if codigo_parte.endswith(":"):
                codigo_parte = codigo_parte[:-1].rstrip()
            linea_salida = codigo_parte + ":" + ((" " + comentario) if comentario else "")
            salida.append("    " * profundidad + linea_salida)
            pila.append(primer_token)
            profundidad += 1
            continue
        salida.append("    " * profundidad + contenido)

    if pila:
        raise LatiPySourceError(f"Falta 'fin' para cerrar {len(pila)} bloque(s). Revisa el final del archivo.")
    return "\n".join(salida) + ("\n" if codigo.endswith("\n") else "")


class LatiPySourceError(Exception):
    """Error de estructura en el archivo LatiPy antes de traducirlo."""


def traducir_codigo(codigo: str) -> str:
    """Traduce palabras reservadas y acepta el modo facil con fin."""
    codigo = _normalizar_bloques_faciles(codigo)
    salida = []
    tokens = tokenize.generate_tokens(io.StringIO(codigo).readline)
    for tok in tokens:
        if tok.type == tokenize.NAME and tok.string in TOKEN_TRANSLATIONS:
            tok = tok._replace(string=TOKEN_TRANSLATIONS[tok.string])
        salida.append(tok)
    return tokenize.untokenize(salida)


def crear_entorno():
    entorno = {"__name__": "__main__", "__builtins__": builtins.__dict__}
    for alias, nombre_python in BUILTIN_ALIASES.items():
        if hasattr(builtins, nombre_python):
            entorno[alias] = getattr(builtins, nombre_python)
    entorno.update(EXTRA_VALUES)
    entorno.update({
        "preguntar_numero": preguntar_numero,
        "preguntar_decimal": preguntar_decimal,
        "numero_aleatorio": numero_aleatorio,
        "elegir_al_azar": elegir_al_azar,
    })
    return entorno


ERROR_TIPS = {
    "NameError": "Un nombre no existe. Revisa como escribiste la variable o funcion.",
    "TypeError": "Se mezclaron tipos de datos que no encajan para esa operacion.",
    "ValueError": "El dato tiene el tipo esperado, pero su valor no sirve para esa operacion.",
    "ZeroDivisionError": "No se puede dividir entre cero.",
    "IndexError": "Intentaste usar una posicion que no existe en la lista o texto.",
    "KeyError": "Esa clave no existe en el diccionario.",
    "FileNotFoundError": "No se encontro el archivo que intentaste abrir.",
    "AttributeError": "Ese objeto no tiene el atributo o metodo que escribiste.",
    "ImportError": "No se pudo importar ese modulo o nombre.",
    "ModuleNotFoundError": "No se encontro ese modulo. Revisa su nombre y si esta instalado.",
    "RecursionError": "La funcion se llamo demasiadas veces a si misma.",
    "AssertionError": "Una comprobacion con 'verificar' no se cumplio.",
}


def _sugerencia_nombre(exc: NameError) -> str | None:
    nombre = getattr(exc, "name", None)
    if not nombre:
        return None
    opciones = list(BUILTIN_ALIASES) + list(TOKEN_TRANSLATIONS) + ["preguntar_numero", "preguntar_decimal", "numero_aleatorio", "elegir_al_azar"]
    coincidencias = difflib.get_close_matches(nombre, opciones, n=1, cutoff=0.68)
    return coincidencias[0] if coincidencias else None


def ejecutar_archivo(ruta: Path, ver_traduccion=False, solo_comprobar=False, mostrar_traza=False) -> int:
    try:
        codigo = ruta.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"No encontre el archivo: {ruta}")
        print("Revisa la ruta y confirma que el archivo termine en .lpy.")
        return 2
    except OSError as exc:
        print(f"No pude leer el archivo: {exc}")
        return 2
    try:
        traducido = traducir_codigo(codigo)
    except LatiPySourceError as exc:
        print(f"Error de estructura en LatiPy: {exc}")
        return 2
    except (tokenize.TokenError, IndentationError) as exc:
        print(f"No pude analizar el codigo: {exc}")
        return 2

    if ver_traduccion:
        print("# Traduccion de LatiPy a Python (vista previa)\n")
        print(traducido, end="" if traducido.endswith("\n") else "\n")
        return 0

    try:
        codigo_compilado = compile(traducido, str(ruta), "exec")
    except SyntaxError as exc:
        print(f"Error de sintaxis en la linea {exc.lineno or '?'}: {exc.msg}")
        if exc.text:
            print(f"  {exc.text.rstrip()}")
        print("Pista: revisa parentesis, comillas, dos puntos, 'fin' y el orden de las instrucciones.")
        return 1

    if solo_comprobar:
        print(f"Correcto: {ruta.name} no tiene errores de sintaxis detectados.")
        print("Aviso: comprobar no ejecuta el programa y no detecta todos los errores posibles.")
        return 0

    entorno = crear_entorno()
    entorno["__file__"] = str(ruta)
    try:
        exec(codigo_compilado, entorno, entorno)
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        return 130
    except Exception as exc:
        linea = getattr(exc, "__traceback__", None)
        # Busca el ultimo marco que pertenezca al archivo .lpy en el traceback.
        linea_usuario = None
        while linea:
            if Path(linea.tb_frame.f_code.co_filename).name == ruta.name:
                linea_usuario = linea.tb_lineno
            linea = linea.tb_next
        print(f"Error al ejecutar en la linea {linea_usuario or '?'}: {type(exc).__name__}: {exc}")
        consejo = ERROR_TIPS.get(type(exc).__name__)
        if consejo:
            print(f"Pista: {consejo}")
        if isinstance(exc, NameError):
            sugerencia = _sugerencia_nombre(exc)
            if sugerencia:
                print(f"Quizas querias escribir: {sugerencia}")
        if mostrar_traza:
            import traceback
            traceback.print_exc()
        else:
            print("Usa --traza para ver el detalle tecnico completo.")
        return 1
    return 0


def _pruebas_rapidas() -> int:
    pruebas = [
        ("traduccion de palabras", lambda: "mostrar(1 and 2)" in traducir_codigo("mostrar(1 y 2)")),
        ("cadenas intactas", lambda: 'mostrar("si_no mostrar y")' in traducir_codigo('mostrar("si_no mostrar y")')),
        ("bloques faciles", lambda: "if x > 2:" in traducir_codigo("si x > 2\n mostrar(x)\nfin\n")),
        ("funciones", lambda: "def suma(a, b):" in traducir_codigo("funcion suma(a, b)\n devolver a + b\nfin\n")),
        ("no cambia comentarios", lambda: "# si x y mostrar" in traducir_codigo("# si x y mostrar\nmostrar(1)")),
        ("alias disponibles", lambda: all(k in crear_entorno() for k in ("mostrar", "preguntar_numero", "numero_aleatorio", "longitud"))),
        ("cierra bloques", lambda: _falla_por_fin_faltante()),
    ]
    fallos = 0
    print(f"LatiPy {VERSION} - pruebas internas")
    for nombre, prueba in pruebas:
        try:
            resultado = bool(prueba())
        except Exception as exc:
            resultado = False
            detalle = f" ({type(exc).__name__}: {exc})"
        else:
            detalle = "" if resultado else ""
        print(f"{'OK' if resultado else 'FALLO'} - {nombre}{detalle}")
        fallos += not resultado
    print(f"Resultado: {len(pruebas) - fallos}/{len(pruebas)} pruebas internas aprobadas.")
    return 0 if fallos == 0 else 1


def _falla_por_fin_faltante():
    try:
        traducir_codigo("si Verdadero\n mostrar('hola')\n")
    except LatiPySourceError as exc:
        return "Falta 'fin'" in str(exc)
    return False


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="latipy",
        description="Ejecuta programas LatiPy (.lpy) en espanol sin tildes.",
        epilog="Ejemplo: python latipy.py ejemplos/hola.lpy",
    )
    parser.add_argument("archivo", nargs="?", help="archivo .lpy que quieres ejecutar")
    parser.add_argument("--ver-traduccion", action="store_true", help="muestra el Python generado sin ejecutarlo")
    parser.add_argument("--comprobar", action="store_true", help="comprueba la sintaxis sin ejecutar el programa")
    parser.add_argument("--traza", action="store_true", help="muestra el traceback tecnico si ocurre un error")
    parser.add_argument("--pruebas", action="store_true", help="ejecuta las pruebas internas de LatiPy")
    parser.add_argument("--version", action="version", version=f"LatiPy {VERSION}")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.pruebas:
        return _pruebas_rapidas()
    if not args.archivo:
        parser.print_help()
        print("\nPara comenzar: python latipy.py ejemplos/hola_facil.lpy")
        return 2
    return ejecutar_archivo(Path(args.archivo), args.ver_traduccion, args.comprobar, args.traza)


if __name__ == "__main__":
    raise SystemExit(main())
