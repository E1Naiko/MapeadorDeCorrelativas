import json
from pathlib import Path
from dataclasses import asdict

from models import Materia


# ==========================================================
# Utilidades
# ==========================================================

def guardar_json(datos, archivo: Path):

    archivo.parent.mkdir(parents=True, exist_ok=True)

    with open(archivo, "w", encoding="utf8") as f:

        json.dump(
            datos,
            f,
            indent=4,
            ensure_ascii=False
        )


def requisito_json(req):
    """
    Convierte un Requisito al formato de exportación.
    """

    salida = {
        "estado": req.estado
    }

    if not req.especial:
        salida["codigo"] = req.codigo
    else:
        salida["especial"] = req.nombre

    return salida


# ==========================================================
# materias.json
# ==========================================================

def exportar_materias(
        materias: dict[str, Materia],
        carpeta="salida"
):

    salida = {}

    for codigo, materia in materias.items():

        datos = asdict(materia)

        datos.pop("requisitos_cursar")
        datos.pop("requisitos_aprobar")
        datos.pop("desbloquea")

        salida[codigo] = datos

    guardar_json(
        salida,
        Path(carpeta) / "materias.json"
    )


# ==========================================================
# correlativas.json
# ==========================================================

def exportar_correlativas(
        materias: dict[str, Materia],
        carpeta="salida"
):

    salida = {}

    for codigo, materia in materias.items():

        datos = {
            "cursar": [],
            "aprobar": []
        }

        # ---------------- CURSAR ----------------

        for opcion in materia.requisitos_cursar:

            lista = []

            for requisito in opcion.requisitos:

                lista.append(
                    requisito_json(requisito)
                )

            datos["cursar"].append(lista)

        # ---------------- APROBAR ----------------

        for opcion in materia.requisitos_aprobar:

            lista = []

            for requisito in opcion.requisitos:

                lista.append(
                    requisito_json(requisito)
                )

            datos["aprobar"].append(lista)

        salida[codigo] = datos

    guardar_json(
        salida,
        Path(carpeta) / "correlativas.json"
    )


# ==========================================================
# desbloqueos.json
# ==========================================================

def exportar_desbloqueos(
        materias: dict[str, Materia],
        carpeta="salida"
):

    salida = {}

    for codigo, materia in materias.items():

        salida[codigo] = sorted(
            materia.desbloquea
        )

    guardar_json(
        salida,
        Path(carpeta) / "desbloqueos.json"
    )


# ==========================================================
# Exportar todo
# ==========================================================

def exportar_todo(
        materias: dict[str, Materia],
        carpeta="salida"
):

    exportar_materias(materias, carpeta)

    exportar_correlativas(materias, carpeta)

    exportar_desbloqueos(materias, carpeta)