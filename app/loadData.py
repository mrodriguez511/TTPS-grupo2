# from flask import session
import datetime
from app.db import db
import csv


from app.models.diagnosticoPresuntivo import diagnosticoPresuntivo
from app.models.resultado import Resultado
from app.models.medicoDerivante import MedicoDerivante
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

    db.session.add(rol1)
    db.session.add(rol2)
    
    


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

    db.session.add(usuario1)
    db.session.add(usuario2)
    cargarConfig()
    cargarObrasSociales()
    cargarPacientes()
    cargarMedicosDerivantes()
    cargarTiposDeEstudio()
    cargarDiagonosticos()

    db.session.commit()


def cargarConfig():
    from app.models.configuracion import Configuracion

    config = Configuracion(
        paginado=10, paleta_AppPublica=1, paleta_AppPrivada=1, ordenacion=True
    )
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
    with open("archivos/Patologias.csv") as data_set:
        reader = csv.reader(data_set)
        #encabezado = next(reader)
        for fila in reader:
            db.session.add(DiagnosticoPresuntivo(nombre=fila))
    db.session.commit()
