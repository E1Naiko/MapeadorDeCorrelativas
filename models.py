from dataclasses import dataclass, field


@dataclass(slots=True)
class Requisito:
    """
    Un requisito individual.

    Puede representar una materia o una condición especial
    como 'Tener 20 actividades'.
    """

    nombre: str
    codigo: str
    estado: str
    especial: bool = False


@dataclass(slots=True)
class Opcion:
    """
    Una opción de correlativas.

    Todos los requisitos de esta lista deben cumplirse.
    Si existen varias opciones, basta con cumplir una.
    """

    requisitos: list[Requisito] = field(default_factory=list)


@dataclass(slots=True)
class Materia:

    # Identificación
    codigo: str
    nombre: str

    # Información general
    modulo: str = ""
    tipo: str = "Materia"
    anio: int | None = None
    periodo: str = ""

    # Estado del alumno
    estado_actual: str = ""
    origen: str = ""

    # Datos administrativos
    creditos: str = ""
    puntaje: str = ""
    cumplimiento: str = ""

    # Correlativas
    requisitos_cursar: list[Opcion] = field(default_factory=list)
    requisitos_aprobar: list[Opcion] = field(default_factory=list)

    # Grafo inverso
    desbloquea: set[str] = field(default_factory=set)