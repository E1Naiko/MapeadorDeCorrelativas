import re


def extraer_nombre_codigo(texto: str) -> tuple[str, str]:
    """
    Extrae el nombre y el código de una materia.

    Ejemplo:
        "Programación II (I1102)"
    devuelve:
        ("Programación II", "I1102")
    """

    texto = texto.strip()

    patron = r"^(.*?)\s*\(([^()]*)\)\s*$"

    m = re.match(patron, texto)

    if m:
        return m.group(1).strip(), m.group(2).strip()

    return texto, ""


def extraer_anio(texto: str) -> int | None:
    """
    Extrae el año de un texto como:

        "Materia 3"

    devuelve:

        3
    """

    m = re.search(r"(\d+)", texto)

    if m:
        return int(m.group(1))

    return None


def limpiar(linea: str) -> str:
    """
    Elimina espacios y saltos de línea.
    """

    return linea.strip()


def es_inicio_materia(linea: str) -> bool:
    """
    Indica si una línea corresponde al inicio de una materia.
    """

    return linea.startswith("- ")


def es_modulo(linea: str) -> bool:
    return linea.startswith("Módulo:")


def es_cumplimiento(linea: str) -> bool:
    return linea.startswith("Cumplimiento:")


def es_para_cursar(linea: str) -> bool:
    return linea.startswith("/Para cursar")


def es_para_aprobar(linea: str) -> bool:
    return linea.startswith("//Para aprobar")


def es_opcion(linea: str) -> bool:
    return linea.startswith("! Opción")


def separar_campos(linea: str) -> list[str]:
    """
    Divide una línea usando '|'.

    También elimina espacios sobrantes.
    """

    return [x.strip() for x in linea.split("|")]


def es_requisito(linea: str) -> bool:
    """
    Un requisito siempre contiene un '|'.

    Ejemplo:

        Programación II (I1102)|Aprobada
    """

    return "|" in linea

def preprocesar_lineas(lineas: list[str]) -> list[str]:
    """
    Normaliza el archivo exportado por SIU.

    Corrige:

    - Materias partidas en dos líneas
    - Estados partidos en dos líneas
    - Elimina líneas vacías repetidas
    """

    resultado = []

    i = 0

    while i < len(lineas):

        linea = lineas[i].rstrip()

        if not linea:
            i += 1
            continue

        #---------------------------------------------
        # Caso:
        #
        # -
        # Programación III....
        #---------------------------------------------

        if linea == "-" and i + 1 < len(lineas):

            resultado.append("- " + lineas[i + 1].strip())

            i += 2
            continue

        #---------------------------------------------
        # Caso:
        #
        # - Taller...|
        # 8 (Promocionado)|Promoción
        #---------------------------------------------

        if (
            linea.startswith("- ")
            and linea.endswith("|")
            and i + 1 < len(lineas)
        ):

            siguiente = lineas[i + 1].strip()

            if "|" in siguiente:

                resultado.append(linea + siguiente)

                i += 2
                continue

        resultado.append(linea.strip())

        i += 1

    return resultado

def es_especial(nombre: str) -> bool:
    """
    Indica si un requisito NO corresponde a una materia.
    
    Una materia tiene formato: "Nombre (CODIGO)"
    Un requisito especial NO tiene ambos paréntesis.
    """

    return not ("(" in nombre and ")" in nombre)