from datetime import datetime


def registrar_respuesta(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("respuesta.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},USUARIO_BLOQUEADO,{usuario}\n")

    return fecha

intentos = {}

with open("eventos.log", "r", encoding="utf-8") as archivo:

    for linea in archivo:

        fecha, tipo, usuario = linea.strip().split(",")

        if tipo == "LOGIN_FALLIDO":

            if usuario not in intentos:
                intentos[usuario] = []

            intentos[usuario].append(fecha)


valores_mttd = []
valores_mttr = []

for usuario, registros in intentos.items():

    if len(registros) >= 3:

        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Intentos fallidos:", len(registros))
        print("Primer intento:", registros[0])
        print("Detección:", registros[2])


        inicio = datetime.strptime(
             registros[0],
             "%Y-%m-%d %H:%M:%S"
        )

        deteccion = datetime.strptime(
             registros[2],
             "%Y-%m-%d %H:%M:%S"
        )

        fecha_respuesta = registrar_respuesta(usuario)

        respuesta = datetime.strptime(
            fecha_respuesta,
            "%Y-%m-%d %H:%M:%S"
        )

        mttr = (respuesta - deteccion).total_seconds()
        print("MTTR:", mttr, "segundos")
        valores_mttr.append(mttr)

        mttd = (deteccion - inicio).total_seconds()
        print("MTTD:", mttd, "segundos")
        valores_mttd.append(mttd)


        print("Acción aplicada: bloqueo de usuario")
        print("Respuesta:", fecha_respuesta)
        print("\n")


if valores_mttd and valores_mttr:
    promedio_mttd = sum(valores_mttd) / len(valores_mttd)
    promedio_mttr = sum(valores_mttr) / len(valores_mttr)

    print("Promedio MTTD:", promedio_mttd, "segundos")
    print("Promedio MTTR:", promedio_mttr, "segundos")