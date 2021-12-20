# from flask import session
import datetime
from app.db import db
import csv

from app.models.diagnosticoPresuntivo import DiagnosticoPresuntivo
from app.models.resultado import Resultado
from app.models.medicoDerivante import MedicoDerivante
from app.models.medicoInformante import MedicoInformante
from app.models.estado import Estado
from app.models.lote import Lote
from app.models.obraSocial import ObraSocial
from app.models.paciente import Paciente
from app.models.tipoEstudio import TipoEstudio
from app.models.user import User
from app.models.rol import Rol
from app.models.estudio import Estudio


def cargarDatos():
    if not db.session.query(User).first():
        carga()


def carga():
    from app.models.user import User
    from app.models.rol import Rol

    rol1 = Rol(name="administrador")
    rol2 = Rol(name="empleado")
    rol3 = Rol(name="paciente")
    rol4 = Rol(name="configurador")

    db.session.add(rol1)
    db.session.add(rol2)
    db.session.add(rol3)
    db.session.add(rol4)

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
        first_name="configurador",
        last_name="uno",
        dni=55555555,
        email="config@gmail.com",
        password="123",
        rol=4,
    )

    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.add(usuario3)
    cargarConfig()
    cargarObrasSociales()
    cargarPacientes()
    cargarMedicosDerivantes()
    cargarMedicosInformantes()
    cargarTiposDeEstudio()
    cargarDiagonosticos()
    cargarEstudios()

    db.session.commit()


def cargarConfig():
    from app.models.configuracion import Configuracion

    config = Configuracion(True)
    db.session.add(config)
    db.session.commit()


def cargarMedicosDerivantes():
    medicosDerivantes = [
        MedicoDerivante("medicoDerivante1", "uno", 1234, "medicoDerivante1@gmail.com"),
        MedicoDerivante("medicoDerivante2", "dos", 2345, "medicoDerivante2@gmail.com"),
        MedicoDerivante("medicoDerivante3", "tres", 3456, "medicoDerivante3@gmail.com"),
        MedicoDerivante(
            "medicoDerivante4", "cuatro", 4567, "medicoDerivante4@gmail.com"
        ),
    ]

    for medico in medicosDerivantes:
        db.session.add(medico)
    db.session.commit()


def cargarMedicosInformantes():
    medicosInformantes = [
        MedicoInformante("medicoInformante1", "uno", 1234),
        MedicoInformante("medicoInformante2", "dos", 2345),
        MedicoInformante("medicoInformante3", "tres", 3456),
        MedicoInformante("medicoInformante4", "cuatro", 4567),
    ]

    for medico in medicosInformantes:
        db.session.add(medico)
    db.session.commit()


def cargarObrasSociales():
    obrasSociales = [
        ObraSocial("IOMA"),
        ObraSocial("OSPE"),
        ObraSocial("Swiss Medical"),
        ObraSocial("OSDE"),
    ]

    for obraSocial in obrasSociales:
        db.session.add(obraSocial)
    db.session.commit()


def cargarPacientes():
    fecha1 = datetime.date(2000, 5, 17)
    fecha2 = datetime.date(1998, 6, 10)

    p1 = Paciente("Paciente1", "uno", 4444, fecha1)

    p2 = Paciente("Paciente2", "dos", 2222, fecha2)

    p1.email = "paciente1@gmail.com"
    p1.telefono = 1111
    p1.direccion = "Calle 45 123"
    p1.resumenHC = "El paciente presenta multiples fracturas desde niño"
    p1.password = 44000000

    p2.email = "paciente2@gmail.com"
    p2.telefono = 45000000
    p2.direccion = "Calle 142 1553"
    p2.resumenHC = (
        "El paciente presenta alteraciones detectadas en su primer año de vida"
    )
    p2.password = 2222

    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()


def cargarTiposDeEstudio():
    tiposDeEstudio = [
        TipoEstudio("Exoma", "Este es el consentimiento del estudio Exoma"),
        TipoEstudio(
            "Genoma mitocondrial completo",
            "Este es el consentimiento del estudio Genoma mitocondrial completo",
        ),
        TipoEstudio(
            "Carrier de enfermedades monogénicas recesivas",
            "Este es el consentimiento del estudio Carrier de enfermedades monogénicas recesivas",
        ),
        TipoEstudio(
            "Cariotipo",
            "Este es el consentimiento del estudio Cariotipo",
        ),
        TipoEstudio(
            "Array CGH",
            "Este es el consentimiento del estudio Array CGH",
        ),
    ]

    for tipoEstudio in tiposDeEstudio:
        db.session.add(tipoEstudio)
    db.session.commit()


def cargarDiagonosticos():
    with open("archivos/Patologias.csv", encoding="utf-8") as data_set:
        reader = csv.reader(data_set)
        for fila in reader:
            db.session.add(DiagnosticoPresuntivo(nombre=fila[0]))
            db.session.commit()


def cargarEstudios():
    estudio1 = Estudio(
        1,  # tipoEstudio hay 5
        2,  # medicoDerivante hay 4
        2,  # paciente hay 2
        2,  # empleado hay 1
        3,  # diagnostico hay muchos 300 y pico
        300000,  # presupuesto
    )

    estudio2 = Estudio(
        1,  # tipoEstudio hay 5
        3,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        10,  # diagnostico hay muchos 300 y pico
        900000,  # presupuesto
    )
    estudio3 = Estudio(
        5,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudio4 = Estudio(
        5,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudioEnero = Estudio(
        5,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudioFebrero = Estudio(
        5,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudioMarzo = Estudio(
        5,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudio5 = Estudio(
        4,  # tipoEstudio hay 5
        3,  # medicoDerivante hay 4
        2,  # paciente hay 2
        2,  # empleado hay 1
        3,  # diagnostico hay muchos 300 y pico
        300000,  # presupuesto
    )

    estudio6 = Estudio(
        4,  # tipoEstudio hay 5
        3,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        10,  # diagnostico hay muchos 300 y pico
        900000,  # presupuesto
    )
    estudio7 = Estudio(
        1,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        18,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudio8 = Estudio(
        3,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        201,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudio9 = Estudio(
        2,  # tipoEstudio hay 5
        3,  # medicoDerivante hay 4
        2,  # paciente hay 2
        2,  # empleado hay 1
        3,  # diagnostico hay muchos 300 y pico
        300000,  # presupuesto
    )

    estudio10 = Estudio(
        4,  # tipoEstudio hay 5
        1,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        10,  # diagnostico hay muchos 300 y pico
        900000,  # presupuesto
    )
    estudio11 = Estudio(
        4,  # tipoEstudio hay 5
        2,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )
    estudio12 = Estudio(
        5,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        2,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        10000,  # presupuesto
    )

    estudio5.estadoActual = 10
    estudio6.estadoActual = 10
    estudio7.estadoActual = 10
    estudio8.estadoActual = 10
    estudio9.estadoActual = 10
    estudio10.estadoActual = 10
    estudio11.estadoActual = 10
    estudio12.estadoActual = 10
    estudio5.turno = "2021-08-01"
    estudio6.turno = "2021-08-01"
    estudio7.turno = "2021-08-01"
    estudio8.turno = "2021-08-01"
    estudio9.turno = "2021-08-01"
    estudio10.turno = "2021-08-01"
    estudio11.turno = "2021-08-01"
    estudio12.turno = "2021-08-01"

    estudioMarzo2 = Estudio(
        4,  # tipoEstudio hay 5
        4,  # medicoDerivante hay 4
        1,  # paciente hay 2
        1,  # empleado hay 1
        300,  # diagnostico hay muchos 300 y pico
        20000,  # presupuesto
    )
    estudio1.estadoActual = 6
    estudio2.estadoActual = 6
    estudio3.estadoActual = 6
    estudio4.estadoActual = 4
    estudio1.turno = "2021-01-18"
    estudio2.turno = "2021-05-18"
    estudio3.turno = "2021-10-18"
    estudio4.turno = "2021-12-18"
    estudioEnero.fecha = "2021-01-01"
    estudioFebrero.fecha = "2021-02-01"
    estudioMarzo.fecha = "2021-02-18"

    estadoEstudio5 = Estado(10, 2, 8)
    estadoEstudio6 = Estado(10, 2, 9)
    estadoEstudio7 = Estado(10, 2, 10)
    estadoEstudio8 = Estado(10, 2, 11)
    estadoEstudio9 = Estado(10, 2, 12)
    estadoEstudio10 = Estado(10, 2, 13)
    estadoEstudio11 = Estado(10, 2, 14)
    estadoEstudio12 = Estado(10, 2, 15)

    db.session.add(estadoEstudio5)
    db.session.add(estadoEstudio6)
    db.session.add(estadoEstudio7)
    db.session.add(estadoEstudio8)
    db.session.add(estadoEstudio9)
    db.session.add(estadoEstudio10)
    db.session.add(estadoEstudio11)
    db.session.add(estadoEstudio12)

    estadoEstudio5.fecha = "2021-08-31"
    estadoEstudio6.fecha = "2021-08-20"
    estadoEstudio7.fecha = "2021-08-25"
    estadoEstudio8.fecha = "2021-11-12"
    estadoEstudio9.fecha = "2021-09-05"
    estadoEstudio10.fecha = "2021-08-29"
    estadoEstudio11.fecha = "2021-09-10"
    estadoEstudio12.fecha = "2021-08-18"

    estudioEnero.fecha = "2020-01-01"
    estudioEnero.mes = 1
    estudioFebrero.fecha = "2021-02-01"
    estudioFebrero.mes = 2
    estudioMarzo.fecha = "2021-03-01"
    estudioMarzo.mes = 3
    estudioMarzo2.fecha = "2021-03-18"
    estudioMarzo2.mes = 3
    estudio1.extraccionAbonada = False
    estudio2.extraccionAbonada = False
    estudio3.extraccionAbonada = False
    estudio4.extraccionAbonada = False
    db.session.add(estudio1)
    db.session.add(estudio2)
    db.session.add(estudio3)
    db.session.add(estudio4)
    db.session.add(estudioEnero)
    db.session.add(estudioFebrero)
    db.session.add(estudioMarzo)
    db.session.add(estudio5)
    db.session.add(estudio6)
    db.session.add(estudio7)
    db.session.add(estudio8)
    db.session.add(estudio9)
    db.session.add(estudio10)
    db.session.add(estudio11)
    db.session.add(estudio12)

    lote1 = Lote()
    lote1.estudios.append(estudio5)
    lote1.estudios.append(estudio6)
    lote2 = Lote()
    lote2.estudios.append(estudio7)
    lote2.url = "https://www.google.com/"
    db.session.add(lote1)
    db.session.add(lote2)
    db.session.commit()
    db.session.add(estudioMarzo2)
