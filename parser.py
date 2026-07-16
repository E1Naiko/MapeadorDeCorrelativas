from models import Materia, Requisito, Opcion
from utils import (
    limpiar,
    separar_campos,
    extraer_nombre_codigo,
    extraer_anio,
    es_inicio_materia,
    es_modulo,
    es_cumplimiento,
    es_para_cursar,
    es_para_aprobar,
    es_opcion,
    es_requisito,
    es_especial,
    preprocesar_lineas,
)


def crear_requisito(linea: str) -> Requisito:
    """
    Convierte una línea como

        Programación II (I1102)|Regularizada

    o

        Tener 20 actividades|aprobadas

    en un objeto Requisito.
    """

    izquierda, estado = linea.split("|", 1)

    nombre, codigo = extraer_nombre_codigo(izquierda)

    return Requisito(
        nombre=nombre,
        codigo=codigo,
        estado=estado.strip(),
        especial=es_especial(izquierda),
    )


def crear_materia(
    campos: list[str],
    modulo: str,
    cumplimiento: str,
) -> Materia:
    """
    Construye un objeto Materia a partir de la línea encabezado.
    """

    nombre, codigo = extraer_nombre_codigo(campos[0])

    tipo = ""
    anio = None
    periodo = ""
    estado = ""
    origen = ""
    creditos = ""
    puntaje = ""

    if len(campos) >= 2:
        tipo = campos[1]
        if "Materia" in tipo:
            anio = extraer_anio(tipo)

    if len(campos) >= 3:
        periodo = campos[2]

    if len(campos) >= 4:
        estado = campos[3]

    if len(campos) >= 5:
        origen = campos[4]

    if len(campos) >= 6:
        creditos = campos[5]

    if len(campos) >= 7:
        puntaje = campos[6]

    return Materia(
        codigo=codigo,
        nombre=nombre,
        modulo=modulo,
        tipo=tipo,
        anio=anio,
        periodo=periodo,
        estado_actual=estado,
        origen=origen,
        creditos=creditos,
        puntaje=puntaje,
        cumplimiento=cumplimiento,
    )


def construir_desbloqueos(materias: dict[str, Materia]) -> None:
    """
    Construye el grafo inverso.
    """

    for materia in materias.values():

        for opcion in materia.requisitos_cursar:

            for requisito in opcion.requisitos:

                if requisito.especial:
                    continue

                if requisito.codigo not in materias:
                    continue

                materias[requisito.codigo].desbloquea.add(
                    materia.codigo
                )


def parsear(ruta: str) -> dict[str, Materia]:

    materias: dict[str, Materia] = {}

    modulo_actual = ""
    cumplimiento_actual = ""

    materia_actual = None

    opcion_actual = None

    modo = None

    with open(ruta, encoding="utf8") as archivo:

        lineas = preprocesar_lineas(archivo.readlines())

    for linea in lineas:

        linea = limpiar(linea)

        if not linea:
            continue

        #-----------------------------------------
        # Módulo
        #-----------------------------------------

        if es_modulo(linea):

            modulo_actual = linea.replace(
                "Módulo:",
                ""
            ).strip()

            continue

        #-----------------------------------------
        # Cumplimiento
        #-----------------------------------------

        if es_cumplimiento(linea):

            cumplimiento_actual = linea.replace(
                "Cumplimiento:",
                ""
            ).strip()

            continue

        #-----------------------------------------
        # Materia
        #-----------------------------------------

        if es_inicio_materia(linea):

            campos = separar_campos(linea[2:])

            materia_actual = crear_materia(
                campos,
                modulo_actual,
                cumplimiento_actual,
            )

            materias[materia_actual.codigo] = materia_actual

            opcion_actual = None
            modo = None

            continue

        #-----------------------------------------
        # Para cursar
        #-----------------------------------------

        if es_para_cursar(linea):

            modo = "cursar"

            opcion_actual = None

            continue

        #-----------------------------------------
        # Para aprobar
        #-----------------------------------------

        if es_para_aprobar(linea):

            modo = "aprobar"

            opcion_actual = None

            continue

        #-----------------------------------------
        # Nueva opción
        #-----------------------------------------

        if es_opcion(linea):

            opcion_actual = Opcion()

            if modo == "cursar":

                materia_actual.requisitos_cursar.append(
                    opcion_actual
                )

            elif modo == "aprobar":

                materia_actual.requisitos_aprobar.append(
                    opcion_actual
                )

            continue

        #-----------------------------------------
        # Requisito
        #-----------------------------------------

        if (
            materia_actual is not None
            and opcion_actual is not None
            and es_requisito(linea)
        ):

            opcion_actual.requisitos.append(
                crear_requisito(linea)
            )

    construir_desbloqueos(materias)

    return materias