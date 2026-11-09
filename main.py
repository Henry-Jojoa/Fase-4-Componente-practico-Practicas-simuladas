print("Bienvenidos al curso de Programación")
print("Universidad Nacional Abierta y a Distancia")
print("Profesora: Yerly Zolandy Parra Villarreal")
"""Sistema integral de clientes, servicios y reservas para Software FJ.

El programa demuestra abstraccion, herencia, polimorfismo, encapsulacion,
parametros opcionales para calcular costos y manejo avanzado de excepciones.
No utiliza bases de datos. Los eventos y errores se guardan en software_fj.log.
"""

# Importa ABC y abstractmethod para definir clases y metodos abstractos.
from abc import ABC, abstractmethod
# Importa datetime para asignar fecha y hora a cada reserva.
from datetime import datetime
# Importa logging para registrar eventos y errores en un archivo.
import logging
# Importa count para generar identificadores consecutivos de reserva.
from itertools import count
# Configura el archivo de registro, el nivel y el formato de cada mensaje.
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)
# Crea el objeto que se utilizara para escribir eventos y errores.
LOGGER = logging.getLogger("SoftwareFJ")


# Define la excepcion base para los errores controlados del sistema.
class ErrorSoftwareFJ(Exception):
    """Excepcion base del sistema Software FJ."""


# Define una excepcion para datos que no cumplen las validaciones.
class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato de entrada es invalido."""


# Define una excepcion para servicios que no pueden reservarse.
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando un servicio no esta disponible."""


# Define una excepcion para cambios de estado no permitidos.
class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando una operacion no es valida para el estado actual."""


# Declara una entidad abstracta con identificador y descripcion obligatoria.
class Entidad(ABC):
    """Clase abstracta general para las entidades principales."""

    # Inicializa el identificador protegido de la entidad.
    def __init__(self, identificador: str) -> None:
        # Valida que el identificador sea texto no vacio.
        if not isinstance(identificador, str) or not identificador.strip():
            # Informa el motivo exacto del error.
            raise DatoInvalidoError("El identificador debe ser un texto no vacio.")
        # Guarda el identificador sin espacios externos.
        self._identificador = identificador.strip()

    # Expone el identificador sin permitir su modificacion directa.
    @property
    def identificador(self) -> str:
        # Devuelve el identificador protegido.
        return self._identificador

    # Obliga a las clases derivadas a proporcionar una descripcion.
    @abstractmethod
    def describir(self) -> str:
        # No implementa comportamiento en la clase abstracta.
        raise NotImplementedError

    # Define una representacion legible comun para todas las entidades.
    def __str__(self) -> str:
        # Utiliza la descripcion polimorfica de la clase concreta.
        return self.describir()
