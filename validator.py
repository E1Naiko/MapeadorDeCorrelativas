from models import Materia


def validar_codigos_vacios(materias: dict[str, Materia]) -> list[str]:
    """
    Comprueba que no existan materias con código vacío.
    """

    errores = []

    for codigo, materia in materias.items():

        if not codigo.strip():

            errores.append(
                f"La materia '{materia.nombre}' no posee código.")

    return errores


def validar_codigos_duplicados(materias: dict[str, Materia]) -> list[str]:
    """
    Comprueba que no existan códigos duplicados.
    """

    errores = []
    codigos_vistos = {}

    for codigo, materia in materias.items():

        if codigo in codigos_vistos:
            errores.append(
                f"Código duplicado '{codigo}': "
                f"'{codigos_vistos[codigo].nombre}' y '{materia.nombre}'.")
        else:
            codigos_vistos[codigo] = materia

    return errores


def validar_referencias(materias: dict[str, Materia]) -> list[str]:
    """
    Comprueba que todas las correlativas existan.
    """

    errores = []

    for materia in materias.values():

        for opcion in materia.requisitos_cursar:

            for requisito in opcion.requisitos:

                if requisito.especial:
                    continue

                if requisito.codigo not in materias:

                    errores.append(
                        f"{materia.codigo}: "
                        f"la correlativa '{requisito.codigo}' no existe."
                    )

        for opcion in materia.requisitos_aprobar:

            for requisito in opcion.requisitos:

                if requisito.especial:
                    continue

                if requisito.codigo not in materias:

                    errores.append(
                        f"{materia.codigo}: "
                        f"la correlativa '{requisito.codigo}' no existe."
                    )

    return errores


def validar_opciones_vacias(materias: dict[str, Materia]) -> list[str]:
    """
    Busca opciones sin requisitos.
    """

    errores = []

    for materia in materias.values():

        for i, opcion in enumerate(materia.requisitos_cursar, start=1):

            if len(opcion.requisitos) == 0:

                errores.append(
                    f"{materia.codigo}: "
                    f"Opción {i} de cursado vacía."
                )

        for i, opcion in enumerate(materia.requisitos_aprobar, start=1):

            if len(opcion.requisitos) == 0:

                errores.append(
                    f"{materia.codigo}: "
                    f"Opción {i} de aprobación vacía."
                )

    return errores


def validar_desbloqueos(materias: dict[str, Materia]) -> list[str]:
    """
    Comprueba que una materia no se desbloquee a sí misma.
    """

    errores = []

    for materia in materias.values():

        if materia.codigo in materia.desbloquea:

            errores.append(
                f"{materia.codigo} se desbloquea a sí misma."
            )

    return errores


def validar(materias: dict[str, Materia]) -> list[str]:
    """
    Ejecuta todas las validaciones.
    """

    errores = []

    errores.extend(validar_codigos_vacios(materias))
    errores.extend(validar_codigos_duplicados(materias))
    errores.extend(validar_referencias(materias))
    errores.extend(validar_opciones_vacias(materias))
    errores.extend(validar_desbloqueos(materias))

    return errores