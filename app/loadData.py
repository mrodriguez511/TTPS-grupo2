# from flask import session
import datetime
from app.db import db
from app.models.medicoDerivante import MedicoDerivante
from app.models.punto_encuentro import Paciente, TipoEstudio, ObraSocial


def cargarDatos():
    from app.models.user import User

    if not db.session.query(User).first():
        carga()


def carga():
    from app.models.user import User
    from app.models.rol import Rol

    rol1 = Rol(name="administrador")
    rol2 = Rol(name="empleado")
    rol3 = Rol(name="medicoInformante")

    db.session.add(rol1)
    db.session.add(rol2)
    db.session.add(rol3)

    db.session.commit()

    usuario1 = User(
        first_name="admin",
        last_name="admin1",
        dni=123456789,
        email="admin@gmail.com",
        password="123",
        rol=1,
    )

    usuario2 = User(
        first_name="empleado1",
        last_name="uno",
        dni=987654321,
        email="emp1@gmail.com",
        password="123",
        rol=2,
    )

    usuario3 = User(
        first_name="medicoInformante",
        last_name="uno",
        dni=11111111,
        email="medicoInformante1@gmail.com",
        password="123",
        rol=3,
    )

    usuario4 = User(
        first_name="medicoInformante",
        last_name="dos",
        dni=11111112,
        email="medicoInformante2@gmail.com",
        password="123",
        rol=3,
    )

    usuario5 = User(
        first_name="medicoInformante",
        last_name="tres",
        dni=11111113,
        email="medicoInformante3@gmail.com",
        password="123",
        rol=3,
    )
    usuario6 = User(
        first_name="medicoInformante",
        last_name="cuatro",
        dni=11111114,
        email="medicoInformante4@gmail.com",
        password="123",
        rol=3,
    )

    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.add(usuario3)
    db.session.add(usuario4)
    db.session.add(usuario5)
    db.session.add(usuario6)
    cargarConfig()
    cargarObrasSociales()
    cargarPacientes()
    cargarMedicosDerivantes()
    cargarPermisos(rol1, rol2)
    cargarPuntosDeEncuentro()
    cargarTiposDeEstudio()

    db.session.commit()


def cargarConfig():
    from app.models.configuracion import Configuracion

    config = Configuracion(
        paginado=10, paleta_AppPublica=1, paleta_AppPrivada=1, ordenacion=True
    )
    db.session.add(config)


def cargarMedicosDerivantes():
    medicosDerivantes = [
        MedicoDerivante("medicoDerivante1", "uno", 1234, "medicoDerivante1@gmail.com"),
        MedicoDerivante("medicoDerivante2", "dos", 2345, "medicoDerivante2@gmail.com"),
        MedicoDerivante("medicoDerivante3", "tres", 3456, "medicoDerivante3@gmail.com"),
        MedicoDerivante(
            "medicoDerivante4", "cuatro", 4567, "medicoDerivante4@gmail.com"
        ),
    ]


def cargarObrasSociales():
    obrasSociales = [
        ObraSocial("IOMA"),
        ObraSocial("OSPE"),
        ObraSocial("Swiss Medical"),
        ObraSocial("OSDE"),
    ]

    for obraSocial in obrasSociales:
        db.session.add(obraSocial)


def cargarPacientes():
    fecha1 = datetime.date(2000, 5, 17)
    fecha2 = datetime.date(2005, 6, 10)

    pacientes = [
        Paciente(
            "Paciente1",
            "uno",
            4444,
            fecha1,
            "paciente1@gmail.com",
            1111,
            "El paciente presenta multiples fracturas desde niño",
            12345,
            1,
        ),
        Paciente(
            "Paciente2",
            "dos",
            2222,
            fecha2,
            "paciente2@gmail.com",
            54321,
            "El paciente presenta alteraciones detectadas en su primer año de vida",
        ),
    ]

    for paciente in pacientes:
        db.session.add(paciente)


def cargarPermisos(rol1, rol2):
    from app.models.permiso import Permiso

    permisos_empleado = [
        Permiso(name="paciente_create"),
        Permiso(name="paciente_new"),
        Permiso(name="paciente_update"),
        Permiso(name="paciente_edit"),
        Permiso(name="paciente_delete"),
        Permiso(name="estudio_create"),
        Permiso(name="estudio_new"),
        Permiso(name="estudio_update"),
        Permiso(name="estudio_edit"),
        Permiso(name="estudio_delete"),
    ]
    permisos_admin = [
        Permiso(name="user_create"),
        Permiso(name="user_new"),
        Permiso(name="user_update"),
        Permiso(name="user_edit"),
        Permiso(name="user_delete"),
    ]

    for per in permisos_admin:
        db.session.add(per)
    for per in permisos_empleado:
        db.session.add(per)

    rol1.permisos = permisos_admin
    rol2.permisos = permisos_empleado


def cargarTiposDeEstudio():
    tiposDeEstudio = [
        TipoEstudio("Exoma", "Este es el consentimiento del estudio Exoma", 2000, 200),
        TipoEstudio(
            "Genoma mitocondrial completo",
            "Este es el consentimiento del estudio Genoma mitocondrial completo",
            3000,
            300,
        ),
        TipoEstudio(
            "Carrier de enfermedades monogénicas recesivas",
            "Este es el consentimiento del estudio Carrier de enfermedades monogénicas recesivas",
            4000,
            400,
        ),
        TipoEstudio(
            "Cariotipo", "Este es el consentimiento del estudio Cariotipo", 5000, 500
        ),
        TipoEstudio(
            "Array CGH", "Este es el consentimiento del estudio Array CGH", 6000, 600
        ),
    ]

    for tipoEstudio in tiposDeEstudio:
        db.session.add(tipoEstudio)


def cargarPuntosDeEncuentro():
    from app.models.punto_encuentro import Punto_encuentro

    punto_encuentro1 = Punto_encuentro(
        nombre="Centro Fomento Los Hornos",
        direccion="137 nro 1100",
        coordenadas="-34.95042, -57.97157",
        telefono=2214502525,
        email="centrofomento@gmail.com",
    )
    punto_encuentro2 = Punto_encuentro(
        nombre="Club Estudiantes de La Plata",
        direccion="54 nro 345",
        coordenadas="-34.91688640798946, -57.991297",
        telefono=2214501212,
        email="clubestudiantes@gmail.com",
    )
    punto_encuentro3 = Punto_encuentro(
        nombre="Estadio Ciudad de La Plata",
        direccion="Av. 25 y Av. 32",
        coordenadas="-34.91375, -57.989028",
        telefono=2215217970,
        email="estadiolp@gba.gob.ar",
    )
    punto_encuentro4 = Punto_encuentro(
        nombre="Teatro Coliseo Podesta",
        direccion="Calle 10 nro 733",
        coordenadas="-34.915667, -57.95575",
        telefono=221424845,
        email=" ",
    )
    punto_encuentro5 = Punto_encuentro(
        nombre="Estadio Juan Carmelo Zerillo",
        direccion="Calle 4 e/ 51 y 53 Nº 979",
        coordenadas="-34.91097, -57.93259",
        telefono=2214222510,
        email=" ",
    )
    punto_encuentro6 = Punto_encuentro(
        nombre="Teatro Argentino",
        direccion="Av. 51 Nº702 e/ 8 y 9",
        coordenadas="-34.91787, -57.9536614",
        telefono=2214291745,
        email="  ",
    )
    punto_encuentro7 = Punto_encuentro(
        nombre="Facultad de Informática",
        direccion="Calle 50 &, Av. 120",
        coordenadas="-34.90348, -57.9398445",
        telefono=2214277270,
        email="difusion@info.unlp.edu.ar ",
    )
    punto_encuentro8 = Punto_encuentro(
        nombre="Facultad de Cs Económicas UNLP",
        direccion="Calle 6 nro 777",
        coordenadas="-34.9125197, -57.9528469",
        telefono=2214236769,
        email="comunicacionfce@econo.unlp.edu.ar ",
    )
    punto_encuentro9 = Punto_encuentro(
        nombre="Consulado General de Italia",
        direccion="Calle 48 rno 869",
        coordenadas="-34.9188192, -57.9591685",
        telefono=2214395500,
        email="segreteria.laplata@esteri.it ",
    )
    punto_encuentro10 = Punto_encuentro(
        nombre="Club Meridiano V°",
        direccion="Calle 67 nro 1080",
        coordenadas="-34.93598922, -57.9454101",
        telefono=2214510357,
        email=" ",
    )
    db.session.add(punto_encuentro10)
    db.session.add(punto_encuentro1)
    db.session.add(punto_encuentro2)
    db.session.add(punto_encuentro3)
    db.session.add(punto_encuentro4)
    db.session.add(punto_encuentro5)
    db.session.add(punto_encuentro6)
    db.session.add(punto_encuentro7)
    db.session.add(punto_encuentro7)
    db.session.add(punto_encuentro9)
