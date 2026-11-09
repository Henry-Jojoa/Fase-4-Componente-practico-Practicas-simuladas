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


# Representa un cliente y encapsula sus datos personales.
class Cliente(Entidad):
    """Cliente con nombre, correo y telefono validados."""

    # Construye un cliente con sus datos principales.
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str) -> None:
        # Inicializa la parte heredada de Entidad.
        super().__init__(identificador)
        # Inicializa atributos privados antes de usar sus propiedades.
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""
        # Asigna el nombre mediante el setter validador.
        self.nombre = nombre
        # Asigna el correo mediante el setter validador.
        self.correo = correo
        # Asigna el telefono mediante el setter validador.
        self.telefono = telefono
        # Registra la creacion correcta del cliente.
        LOGGER.info("Cliente creado: %s", self.identificador)

    # Permite consultar el nombre encapsulado.
    @property
    def nombre(self) -> str:
        # Devuelve el nombre privado.
        return self.__nombre

    # Permite modificar el nombre solo si es valido.
    @nombre.setter
    def nombre(self, valor: str) -> None:
        # Comprueba que tenga al menos tres caracteres utiles.
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            # Detiene la operacion con una excepcion personalizada.
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        # Guarda el nombre normalizado.
        self.__nombre = valor.strip().title()

    # Permite consultar el correo encapsulado.
    @property
    def correo(self) -> str:
        # Devuelve el correo privado.
        return self.__correo

    # Permite modificar el correo solo si tiene formato basico valido.
    @correo.setter
    def correo(self, valor: str) -> None:
        # Comprueba elementos esenciales de una direccion de correo.
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            # Informa que el correo suministrado no es valido.
            raise DatoInvalidoError("El correo no tiene un formato valido.")
        # Guarda el correo en minusculas.
        self.__correo = valor.strip().lower()

    # Permite consultar el telefono encapsulado.
    @property
    def telefono(self) -> str:
        # Devuelve el telefono privado.
        return self.__telefono

    # Permite modificar el telefono si contiene entre 7 y 15 digitos.
    @telefono.setter
    def telefono(self, valor: str) -> None:
        # Convierte el dato a texto y retira espacios.
        texto = str(valor).strip()
        # Verifica que solo haya digitos y que la longitud sea adecuada.
        if not texto.isdigit() or not 7 <= len(texto) <= 15:
            # Informa el requisito incumplido.
            raise DatoInvalidoError("El telefono debe contener entre 7 y 15 digitos.")
        # Guarda el telefono validado.
        self.__telefono = texto

    # Implementa el metodo abstracto heredado.
    def describir(self) -> str:
        # Devuelve una descripcion segura del cliente.
        return f"Cliente {self.nombre} (ID: {self.identificador})"


# Define la estructura comun de todos los servicios.
class Servicio(Entidad, ABC):
    """Clase abstracta para los servicios de Software FJ."""

    # Inicializa los datos comunes de un servicio.
    def __init__(self, identificador: str, nombre: str, disponible: bool = True) -> None:
        # Inicializa el identificador heredado.
        super().__init__(identificador)
        # Valida el nombre del servicio.
        if not isinstance(nombre, str) or not nombre.strip():
            # Informa que el nombre es obligatorio.
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        # Guarda el nombre publico normalizado.
        self.nombre = nombre.strip()
        # Guarda la disponibilidad como valor booleano privado.
        self.__disponible = bool(disponible)

    # Permite consultar si el servicio esta disponible.
    @property
    def disponible(self) -> bool:
        # Devuelve la disponibilidad privada.
        return self.__disponible

    # Permite cambiar la disponibilidad de forma controlada.
    def cambiar_disponibilidad(self, disponible: bool) -> None:
        # Valida que se reciba especificamente un booleano.
        if not isinstance(disponible, bool):
            # Rechaza valores ambiguos.
            raise DatoInvalidoError("La disponibilidad debe ser True o False.")
        # Actualiza el estado privado.
        self.__disponible = disponible
        # Registra el cambio realizado.
        LOGGER.info("Disponibilidad de %s cambiada a %s", self.identificador, disponible)

    # Valida los parametros generales antes de reservar.
    def validar_parametros(self, duracion: float) -> None:
        # Impide reservar un servicio marcado como no disponible.
        if not self.disponible:
            # Lanza la excepcion especifica correspondiente.
            raise ServicioNoDisponibleError(f"El servicio {self.nombre} no esta disponible.")
        # Exige una duracion numerica mayor que cero.
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            # Informa que la duracion recibida no es valida.
            raise DatoInvalidoError("La duracion debe ser un numero mayor que cero.")

    # Declara el calculo polimorfico que implementara cada servicio.
    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        # No calcula costos en la clase abstracta.
        raise NotImplementedError


# Implementa el servicio especializado de reserva de salas.
class ReservaSala(Servicio):
    """Servicio de sala cobrado por hora y capacidad."""

    # Construye una sala con tarifa y capacidad.
    def __init__(self, identificador: str, tarifa_hora: float, capacidad: int, disponible: bool = True) -> None:
        # Inicializa los datos comunes del servicio.
        super().__init__(identificador, "Reserva de sala", disponible)
        # Valida una tarifa positiva.
        if tarifa_hora <= 0:
            # Rechaza una tarifa inconsistente.
            raise DatoInvalidoError("La tarifa de la sala debe ser mayor que cero.")
        # Valida una capacidad entera positiva.
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            # Rechaza una capacidad inconsistente.
            raise DatoInvalidoError("La capacidad debe ser un entero mayor que cero.")
        # Guarda la tarifa por hora.
        self.tarifa_hora = float(tarifa_hora)
        # Guarda la capacidad maxima.
        self.capacidad = capacidad

    # Calcula el costo con parametros opcionales equivalentes a sobrecarga en Python.
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        # Valida disponibilidad y duracion.
        self.validar_parametros(duracion)
        # Delega la formula comun a una funcion segura.
        return aplicar_ajustes(self.tarifa_hora * duracion, impuesto, descuento)

    # Describe las caracteristicas particulares de la sala.
    def describir(self) -> str:
        # Devuelve la descripcion polimorfica.
        return f"Sala para {self.capacidad} personas a ${self.tarifa_hora:,.0f} por hora"


# Implementa el servicio especializado de alquiler de equipos.
class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos cobrado por dia."""

    # Construye el servicio de alquiler.
    def __init__(self, identificador: str, equipo: str, tarifa_dia: float, disponible: bool = True) -> None:
        # Inicializa los datos comunes.
        super().__init__(identificador, "Alquiler de equipo", disponible)
        # Valida que el equipo tenga nombre.
        if not isinstance(equipo, str) or not equipo.strip():
            # Rechaza un nombre vacio.
            raise DatoInvalidoError("El nombre del equipo es obligatorio.")
        # Valida que la tarifa sea positiva.
        if tarifa_dia <= 0:
            # Rechaza una tarifa invalida.
            raise DatoInvalidoError("La tarifa diaria debe ser mayor que cero.")
        # Guarda el nombre del equipo.
        self.equipo = equipo.strip()
        # Guarda la tarifa diaria.
        self.tarifa_dia = float(tarifa_dia)

    # Calcula el costo del alquiler con ajustes opcionales.
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        # Valida la solicitud.
        self.validar_parametros(duracion)
        # Calcula y ajusta el valor base.
        return aplicar_ajustes(self.tarifa_dia * duracion, impuesto, descuento)

    # Describe el equipo y su tarifa.
    def describir(self) -> str:
        # Devuelve la descripcion especializada.
        return f"Alquiler de {self.equipo} a ${self.tarifa_dia:,.0f} por dia"
