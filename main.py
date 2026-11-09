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


# Implementa el servicio especializado de asesoria.
class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria cobrado por hora y nivel."""

    # Define factores permitidos para cada nivel de asesoria.
    FACTORES = {"basica": 1.0, "intermedia": 1.25, "avanzada": 1.5}

    # Construye una asesoria con tarifa y nivel.
    def __init__(self, identificador: str, tarifa_hora: float, nivel: str, disponible: bool = True) -> None:
        # Inicializa los datos comunes.
        super().__init__(identificador, "Asesoria especializada", disponible)
        # Normaliza el nivel recibido.
        nivel_normalizado = str(nivel).strip().lower()
        # Verifica que el nivel figure en el catalogo permitido.
        if nivel_normalizado not in self.FACTORES:
            # Informa los niveles aceptados.
            raise DatoInvalidoError("El nivel debe ser basica, intermedia o avanzada.")
        # Valida una tarifa positiva.
        if tarifa_hora <= 0:
            # Rechaza una tarifa inconsistente.
            raise DatoInvalidoError("La tarifa de asesoria debe ser mayor que cero.")
        # Guarda la tarifa por hora.
        self.tarifa_hora = float(tarifa_hora)
        # Guarda el nivel validado.
        self.nivel = nivel_normalizado

    # Calcula el costo segun tarifa, duracion y nivel.
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        # Valida la solicitud.
        self.validar_parametros(duracion)
        # Calcula el subtotal segun el factor del nivel.
        subtotal = self.tarifa_hora * duracion * self.FACTORES[self.nivel]
        # Aplica impuesto y descuento opcionales.
        return aplicar_ajustes(subtotal, impuesto, descuento)

    # Describe el nivel y la tarifa de la asesoria.
    def describir(self) -> str:
        # Devuelve la descripcion especializada.
        return f"Asesoria {self.nivel} a ${self.tarifa_hora:,.0f} por hora base"


# Centraliza la validacion de impuestos y descuentos.
def aplicar_ajustes(subtotal: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
    # Valida que el subtotal no sea negativo.
    if subtotal < 0:
        # Evita calculos financieros inconsistentes.
        raise DatoInvalidoError("El subtotal no puede ser negativo.")
    # Valida porcentajes entre cero y cien.
    if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
        # Rechaza porcentajes que producirian resultados incoherentes.
        raise DatoInvalidoError("Impuesto y descuento deben estar entre 0 y 100.")
    # Aplica primero el descuento y luego el impuesto.
    total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)
    # Devuelve el total redondeado a dos decimales.
    return round(total, 2)


# Integra un cliente, un servicio, una duracion y un estado.
class Reserva(Entidad):
    """Reserva con confirmacion, procesamiento y cancelacion controlados."""

    # Crea un contador compartido para identificadores consecutivos.
    _consecutivo = count(1)

    # Construye una reserva en estado pendiente.
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float) -> None:
        # Genera e inicializa el identificador heredado.
        super().__init__(f"R-{next(self._consecutivo):04d}")
        # Verifica que el cliente sea del tipo esperado.
        if not isinstance(cliente, Cliente):
            # Rechaza objetos que no representen clientes.
            raise DatoInvalidoError("La reserva requiere un cliente valido.")
        # Verifica que el servicio derive de Servicio.
        if not isinstance(servicio, Servicio):
            # Rechaza objetos que no representen servicios.
            raise DatoInvalidoError("La reserva requiere un servicio valido.")
        # Valida disponibilidad y duracion antes de guardar la reserva.
        servicio.validar_parametros(duracion)
        # Guarda el cliente asociado.
        self.cliente = cliente
        # Guarda el servicio asociado.
        self.servicio = servicio
        # Guarda la duracion como decimal.
        self.duracion = float(duracion)
        # Inicializa el estado de la reserva.
        self.estado = "PENDIENTE"
        # Registra la fecha y hora de creacion.
        self.fecha_creacion = datetime.now()
        # Registra el evento correcto.
        LOGGER.info("Reserva %s creada para %s", self.identificador, cliente.identificador)

    # Confirma una reserva pendiente.
    def confirmar(self) -> None:
        # Impide confirmar una reserva que ya cambio de estado.
        if self.estado != "PENDIENTE":
            # Informa la operacion no permitida.
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        # Revalida el servicio antes de confirmar.
        self.servicio.validar_parametros(self.duracion)
        # Actualiza el estado.
        self.estado = "CONFIRMADA"
        # Registra la confirmacion.
        LOGGER.info("Reserva %s confirmada", self.identificador)

    # Procesa una reserva confirmada y calcula su costo.
    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        # Exige confirmacion previa.
        if self.estado != "CONFIRMADA":
            # Rechaza el procesamiento fuera de secuencia.
            raise OperacionNoPermitidaError("Solo se procesan reservas confirmadas.")
        # Calcula el costo mediante polimorfismo.
        total = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
        # Cambia el estado luego de un calculo exitoso.
        self.estado = "PROCESADA"
        # Registra el total procesado.
        LOGGER.info("Reserva %s procesada por %.2f", self.identificador, total)
        # Entrega el total calculado.
        return total

    # Cancela una reserva que aun no haya sido procesada.
    def cancelar(self) -> None:
        # Impide cancelar reservas finalizadas.
        if self.estado in {"PROCESADA", "CANCELADA"}:
            # Informa el estado incompatible.
            raise OperacionNoPermitidaError("No es posible cancelar una reserva finalizada.")
        # Actualiza el estado.
        self.estado = "CANCELADA"
        # Registra la cancelacion.
        LOGGER.info("Reserva %s cancelada", self.identificador)

    # Describe la reserva con sus relaciones principales.
    def describir(self) -> str:
        # Devuelve un resumen legible.
        return f"{self.identificador}: {self.cliente.nombre} - {self.servicio.nombre} - {self.estado}"


# Administra listas internas sin utilizar una base de datos.
class SistemaGestion:
    """Contenedor en memoria para clientes, servicios y reservas."""

    # Inicializa las listas internas del sistema.
    def __init__(self) -> None:
        # Crea la lista de clientes.
        self.clientes: list[Cliente] = []
        # Crea la lista de servicios.
        self.servicios: list[Servicio] = []
        # Crea la lista de reservas.
        self.reservas: list[Reserva] = []

    # Registra un cliente evitando identificadores repetidos.
    def agregar_cliente(self, cliente: Cliente) -> None:
        # Busca previamente el identificador en la lista.
        if any(item.identificador == cliente.identificador for item in self.clientes):
            # Rechaza el duplicado.
            raise DatoInvalidoError("Ya existe un cliente con ese identificador.")
        # Agrega el objeto valido a la lista.
        self.clientes.append(cliente)

    # Registra un servicio evitando identificadores repetidos.
    def agregar_servicio(self, servicio: Servicio) -> None:
        # Busca previamente el identificador en la lista.
        if any(item.identificador == servicio.identificador for item in self.servicios):
            # Rechaza el duplicado.
            raise DatoInvalidoError("Ya existe un servicio con ese identificador.")
        # Agrega el objeto valido a la lista.
        self.servicios.append(servicio)

    # Crea y almacena una nueva reserva.
    def crear_reserva(self, cliente: Cliente, servicio: Servicio, duracion: float) -> Reserva:
        # Construye la reserva con sus validaciones.
        reserva = Reserva(cliente, servicio, duracion)
        # Guarda la reserva en memoria.
        self.reservas.append(reserva)
        # Devuelve el objeto para operaciones posteriores.
        return reserva

    # Define una representacion legible del estado general del sistema.
    def __str__(self) -> str:
        # Resume las cantidades almacenadas en las listas internas.
        return (
            f"SistemaGestion(clientes={len(self.clientes)}, "
            f"servicios={len(self.servicios)}, reservas={len(self.reservas)})"
        )


# Ejecuta una operacion y evita que un error detenga la demostracion.
def ejecutar_operacion(numero: int, titulo: str, funcion) -> object | None:
    # Muestra el encabezado de la operacion actual.
    print(f"\nOperacion {numero}: {titulo}")
    # Inicia el bloque de manejo de errores.
    try:
        # Ejecuta la funcion recibida y guarda su resultado.
        resultado = funcion()
    # Captura primero las excepciones controladas del proyecto.
    except ErrorSoftwareFJ as error:
        # Registra el error con su traza para auditoria.
        LOGGER.exception("Operacion %s controlada con error: %s", numero, error)
        # Informa el error sin cerrar la aplicacion.
        print(f"ERROR CONTROLADO: {error}")
        # Indica que no hubo resultado valido.
        return None
    # Captura cualquier error inesperado como proteccion adicional.
    except Exception as error:
        # Crea y encadena una excepcion del dominio.
        try:
            # Lanza un error profesional conservando la causa original.
            raise ErrorSoftwareFJ("Ocurrio un error inesperado en la operacion.") from error
        # Captura el error encadenado para registrarlo.
        except ErrorSoftwareFJ as error_encadenado:
            # Registra la cadena completa de excepciones.
            LOGGER.exception("Operacion %s con error inesperado", numero)
            # Informa el error controlado al usuario.
            print(f"ERROR INESPERADO CONTROLADO: {error_encadenado}")
            # Indica que no hubo resultado valido.
            return None
    # Se ejecuta solamente cuando no ocurrio ninguna excepcion.
    else:
        # Registra el exito de la operacion.
        LOGGER.info("Operacion %s finalizada correctamente", numero)
        # Muestra el resultado si tiene contenido.
        print("RESULTADO:", resultado if resultado is not None else "Operacion exitosa")
        # Devuelve el resultado exitoso.
        return resultado
    # Se ejecuta tanto con exito como con error.
    finally:
        # Muestra que el sistema continua disponible.
        print("Estado: operacion finalizada; el sistema continua activo.")


# Ejecuta al menos diez operaciones validas e invalidas de forma secuencial.
def demostracion() -> None:
    # Muestra el titulo principal.
    print("SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    # Registra el inicio de la demostracion.
    LOGGER.info("Inicio de la demostracion secuencial")
    # Crea el administrador en memoria.
    sistema = SistemaGestion()

    # Crea correctamente el primer cliente.
    cliente_1 = ejecutar_operacion(1, "Registrar cliente valido", lambda: Cliente("C001", "Ana Torres", "ana@correo.com", "3101234567"))
    # Agrega el cliente si la operacion fue exitosa.
    if cliente_1:
        sistema.agregar_cliente(cliente_1)

    # Intenta crear un cliente con correo invalido.
    ejecutar_operacion(2, "Registrar cliente con correo invalido", lambda: Cliente("C002", "Luis Perez", "correo-invalido", "3111234567"))

    # Intenta crear un cliente con telefono invalido.
    ejecutar_operacion(3, "Registrar cliente con telefono invalido", lambda: Cliente("C003", "Marta Ruiz", "marta@correo.com", "12A"))

    # Crea correctamente el servicio de sala.
    sala = ejecutar_operacion(4, "Crear servicio de sala valido", lambda: ReservaSala("S001", 50000, 12))
    # Agrega la sala si fue creada.
    if sala:
        sistema.agregar_servicio(sala)

    # Intenta crear un alquiler con tarifa negativa.
    ejecutar_operacion(5, "Crear equipo con tarifa invalida", lambda: AlquilerEquipo("S002", "Portatil", -1000))

    # Crea correctamente un alquiler de equipo.
    equipo = ejecutar_operacion(6, "Crear alquiler de equipo valido", lambda: AlquilerEquipo("S003", "Video beam", 80000))
    # Agrega el equipo si fue creado.
    if equipo:
        sistema.agregar_servicio(equipo)

    # Crea correctamente una asesoria avanzada.
    asesoria = ejecutar_operacion(7, "Crear asesoria valida", lambda: AsesoriaEspecializada("S004", 90000, "avanzada"))
    # Agrega la asesoria si fue creada.
    if asesoria:
        sistema.agregar_servicio(asesoria)

    # Crea una reserva valida de sala.
    reserva_1 = ejecutar_operacion(8, "Crear reserva valida", lambda: sistema.crear_reserva(cliente_1, sala, 2))

    # Confirma la reserva creada.
    if reserva_1:
        ejecutar_operacion(9, "Confirmar reserva", reserva_1.confirmar)

    # Procesa la reserva con impuesto y descuento opcionales.
    if reserva_1:
        ejecutar_operacion(10, "Procesar con IVA 19% y descuento 10%", lambda: reserva_1.procesar(impuesto=19, descuento=10))

    # Intenta cancelar una reserva ya procesada.
    if reserva_1:
        ejecutar_operacion(11, "Cancelar reserva procesada", reserva_1.cancelar)

    # Deshabilita el alquiler para probar disponibilidad.
    if equipo:
        equipo.cambiar_disponibilidad(False)
        ejecutar_operacion(12, "Reservar servicio no disponible", lambda: sistema.crear_reserva(cliente_1, equipo, 1))

    # Intenta reservar con duracion negativa.
    if asesoria:
        ejecutar_operacion(13, "Reservar con duracion invalida", lambda: sistema.crear_reserva(cliente_1, asesoria, -2))

    # Crea y cancela correctamente otra reserva.
    reserva_2 = ejecutar_operacion(14, "Crear reserva de asesoria", lambda: sistema.crear_reserva(cliente_1, asesoria, 3))
    # Cancela la reserva pendiente para demostrar el flujo alternativo.
    if reserva_2:
        ejecutar_operacion(15, "Cancelar reserva pendiente", reserva_2.cancelar)

    # Muestra el resumen final de objetos almacenados.
    print("\nRESUMEN FINAL")
    # Muestra el total de clientes validos.
    print(f"Clientes almacenados: {len(sistema.clientes)}")
    # Muestra el total de servicios validos.
    print(f"Servicios almacenados: {len(sistema.servicios)}")
    # Muestra el total de reservas creadas correctamente.
    print(f"Reservas almacenadas: {len(sistema.reservas)}")
    # Informa la ubicacion relativa del archivo de log.
    print("Eventos y errores registrados en: software_fj.log")
    # Registra la terminacion normal del programa.
    LOGGER.info("Fin de la demostracion secuencial")


if __name__ == "__main__":
    # Inicia la demostracion completa del sistema.
    demostracion()
