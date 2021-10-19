# from flask import session
from app.db import db


def cargarDatos():
    from app.models.user import User
    if not db.session.query(User).first():
        carga()


def carga():
    from app.models.user import User
    from app.models.rol import Rol

    rol1 = Rol(name="administrador")
    rol2 = Rol(name="operador")

    usuario1 = User(
        first_name="Mariana",
        last_name="Rodriguez",
        email="mari_r@gmail.com",
        password="123",
        username="mari_r",
    )

    usuario2 = User(
        first_name="Iona",
        last_name="Arregui",
        email="iona@gmail.com",
        password="123",
        username="iona",
    )

    usuario3 = User(
        first_name="Mariana",
        last_name="Jobse",
        email="mari_j@gmail.com",
        password="123",
        username="mari_j",
    )
    usuario4 = User(
        first_name="Damian ",
        last_name="Candia",
        email="damian@gmail.com",
        password="123",
        username="damian",
    )

    db.session.add(rol1)
    db.session.add(rol2)

    usuario1.roles = [rol1]
    usuario2.roles = [rol2]
    usuario3.roles = [rol2]
    usuario4.roles = [rol2]

    db.session.add(usuario1)
    db.session.add(usuario2)
    db.session.add(usuario3)
    db.session.add(usuario4)
    cargarConfig()
    cargarPermisos(rol1, rol2)
    cargarPuntosDeEncuentro()

    db.session.commit()


def cargarConfig():
    from app.models.configuracion import Configuracion

    config = Configuracion(
        paginado=10, paleta_AppPublica=1, paleta_AppPrivada=1, ordenacion=True
    )
    db.session.add(config)


def cargarPermisos(rol1, rol2):
    from app.models.permiso import Permiso

    permisos_ambos = [
        Permiso(name="user_index"),
        Permiso(name="punto_encuentro_index"),
        Permiso(name="punto_encuentro_create"),
        Permiso(name="punto_encuentro_new"),
        Permiso(name="punto_encuentro_edit"),
        Permiso(name="punto_encuentro_update"),
        Permiso(name="punto_encuentro_show"),
    ]
    permisos_admin = [
        Permiso(name="user_create"),
        Permiso(name="user_new"),
        Permiso(name="user_update"),
        Permiso(name="user_edit"),
        Permiso(name="user_delete"),
        Permiso(name="user_swichtstate"),
        Permiso(name="rol_asignar"),
        Permiso(name="configuracion_edit"),
        Permiso(name="configuracion_update"),
        Permiso(name="punto_encuentro_destroy"),
    ]

    for per in permisos_ambos:
        db.session.add(per)
    for per in permisos_admin:
        db.session.add(per)

    rol1.permisos = permisos_admin
    for per in permisos_ambos:
        rol1.permisos.append(per)
    rol2.permisos = permisos_ambos


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
