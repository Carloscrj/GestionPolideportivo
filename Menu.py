import psycopg2
import psycopg2.extras

import Cliente


# Conexion a la base de datos en PostgreSQL

print("Conectando a la base de datos...")

conx = None

try:
    conx = psycopg2.connect(dbname="postgres", user="postgres", password="Perritos_Rams12", port="5432")
    print("Estableciendo conexión...")
    cur = conx.cursor()
    print("Conexión establecida")
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Version de PostgreSQL: \n", version)

    # Creación de tablas
    cur.execute("DROP TABLE IF EXISTS MATRICULAS")
    cur.execute("DROP TABLE IF EXISTS CLIENTES")
    cur.execute("DROP TABLE IF EXISTS DEPORTES")

    print("La tablas han sido eliminadas")

    cur.execute("CREATE TABLE CLIENTES (id serial PRIMARY KEY, "
                   "NOMBRE VARCHAR, APELLIDOS VARCHAR, DNI VARCHAR, "
                   "FECHA_NAC VARCHAR, TELEFONO VARCHAR)")
    print("Tabla clientes creada.")


    cur.execute("CREATE TABLE DEPORTES (id serial PRIMARY KEY, "
                   "NOMBRE VARCHAR, PRECIO INTEGER)")
    print("Tabla deportes creada.")
    cur.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("FUTBOL", 60))
    cur.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("BALONCESTO", 55))
    cur.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("TENIS", 80))
    cur.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("ATLETISMO", 25))
    cur.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("NATACION", 35))

    cur.execute("CREATE TABLE MATRICULAS (ID_CLIENTE INTEGER, ID_DEPORTE INTEGER, HORARIO VARCHAR,"
                   "CONSTRAINT FK_CLI FOREIGN KEY(ID_CLIENTE) REFERENCES CLIENTES(id) ON DELETE CASCADE,"
                   "CONSTRAINT FK_DEPO FOREIGN KEY(ID_DEPORTE) REFERENCES DEPORTES(id),"
                   "CONSTRAINT PK_MAT PRIMARY KEY(ID_CLIENTE, ID_DEPORTE))")
    print("Tabla matriculas creada.")

    conx.commit()
    print("Tablas creadas correctamente")
    cur.close()


except (Exception, psycopg2.DatabaseError) as error:
    print("Error de excepción ", error)



def dar_alta_cliente():
    try:
        print("Introduzca el nombre del cliente")
        nombre = input()
        print("Introduzca los apellidos del cliente")
        apellidos = input()
        print("Introduzca el dni del cliente")
        dni = input()
        cur = conx.cursor()
        cur.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conx.commit()
        cliente = cur.fetchone()  # se comprueba que el cliente existe con ese dni
        if cliente is None:
            print("Introduzca la fecha de nacimiento del cliente")
            fecha_nacimiento = input()
            print("Introduzca el teléfono del cliente")
            telefono = input()
            # Se insertan los datos en la tabla CLIENTES
            cur.execute("INSERT INTO CLIENTES (NOMBRE, APELLIDOS, DNI, FECHA_NAC, TELEFONO) VALUES (%s, %s, %s, %s, %s)",
                        (nombre, apellidos, dni, fecha_nacimiento, telefono))
            conx.commit()
            print("Cliente dado de alta correctamente")
        else:
            print("El cliente ya existe")

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


def dar_baja_cliente():
    try:
        print("Introduzca el dni del cliente para darlo de baja")
        dni = input()

        cur = conx.cursor()
        # Se borran los datos de la tabla CLIENTES que coincidan con el dni introducido
        cur.execute("DELETE FROM CLIENTES WHERE DNI = %s", (dni,))
        conx.commit()
        print("Cliente dado de baja correctamente")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


def mostrar_todos_clientes():
    try:
        cur = conx.cursor()
        cur.execute("SELECT * FROM CLIENTES")
        conx.commit()
        clientes = cur.fetchall()
        if not clientes:
            print("No hay clientes")
        else:
            for cliente in clientes:
                cliente = Cliente.Cliente(cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
                print(cliente.__datos__())
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


def mostrar_un_cliente():
    try:
        print("Introduzca el dni del cliente para mostrar sus datos")
        dni = input()

        cur = conx.cursor()
        # Se muestran los datos de la tabla CLIENTES que coincidan con el dni introducido
        cur.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conx.commit()
        cliente = cur.fetchone()
        if cliente is None:
            print("No hay clientes con ese dni")
        else:
            cliente = Cliente.Cliente(cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
            print(cliente.__datos__())
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


def mostrar_datos_cliente(): #aquí usamos la clase cliente
    # Se muestra un menú para elegir si se quieren mostrar todos los clientes o solo uno
    print("Introduzca 1 para mostrar todos los clientes o 2 para mostrar solo un cliente")
    opcion = int(input())
    if opcion == 1:
        mostrar_todos_clientes()
    elif opcion == 2:
        mostrar_un_cliente()
    else:
        print("Opción incorrecta")


def matricular_cliente():
    try:
        dicc_deportes_horarios = {
            'FUTBOL': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
            'BALONCESTO': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
            'TENIS': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
            'ATLETISMO': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
            'NATACION': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00']
        }

        print("Introduzca el dni del cliente para matricularlo en un deporte")
        dni = input()
        cur = conx.cursor()
        cur.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conx.commit()
        cliente = cur.fetchone() #se comprueba que el cliente existe con ese dni

        if cliente is None:
            print("No hay clientes con ese dni")
        else:
            id = cliente[0]
            print("Introduzca el nombre del deporte")
            deporte = input()
            deporte = deporte.upper()
            if deporte not in dicc_deportes_horarios:
                    print("No hay deportes con ese nombre")
            else:
                print("Introduzca el horario")
                horario = input()
                if horario not in dicc_deportes_horarios[deporte]:
                    print("No hay horarios con ese deporte")
                else:
                    cur = conx.cursor()
                    cur.execute("SELECT * FROM DEPORTES WHERE NOMBRE= %s", (deporte,))
                    conx.commit()
                    deporte = cur.fetchone()
                    id_deporte = deporte[0]

                    # Se insertan los datos en la tabla MATRICULAS
                    cur.execute("INSERT INTO MATRICULAS (ID_CLIENTE, ID_DEPORTE, HORARIO) VALUES (%s, %s, %s)", (id, id_deporte, horario))
                    conx.commit()
                    print("Cliente matriculado correctamente")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


def borrar_matricula_cliente():
    try:
        print("Introduzca el dni del cliente para borrar matricula del deporte")
        dni = input()
        cur = conx.cursor()
        cur.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conx.commit()
        cliente = cur.fetchone()  # se comprueba que el cliente existe con ese dni

        if cliente is None:
            print("No hay clientes con ese dni")
        else:
            id = cliente[0]
            cur.execute("SELECT * FROM MATRICULAS WHERE ID_CLIENTE = %s", (id,))
            conx.commit()
            matriculas = cur.fetchall()
            if matriculas is None:
                print("No hay matriculas")
            else:
                print("Deportes en los que está matriculado el cliente")
                deportes_matriculado = []
                for matricula in matriculas:
                    cur.execute("SELECT * FROM DEPORTES WHERE ID = %s", (matricula[1],))
                    conx.commit()
                    deporte = cur.fetchone()
                    print("Deporte: " + deporte[1] + " Horario: " + matricula[2])
                    deportes_matriculado.append(deporte[1].upper())

            print("Introduzca el nombre del deporte en el que está matriculado el cliente")
            deporte = input()
            deporte = deporte.upper()
            if deporte not in deportes_matriculado:
                print("No está matriculado en ese deporte.")
            else:
                cur.execute("SELECT * FROM DEPORTES WHERE NOMBRE= %s", (deporte,))
                conx.commit()
                deporte = cur.fetchone()
                id_deporte = deporte[0]
                cur.execute("DELETE FROM MATRICULAS WHERE ID_CLIENTE = %s AND ID_DEPORTE = %s", (id, id_deporte))
                conx.commit()
                print("Deporte borrado de ese cliente.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


def mostrar_deportes_cliente():
    try:
        print("Introduzca el dni del cliente para mostrar sus deportes")
        dni = input()
        cur = conx.cursor()
        cur.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conx.commit()
        cliente = cur.fetchone()  # se comprueba que el cliente existe con ese dni

        if cliente is None:
            print("No hay clientes con ese dni")
        else:
            id = cliente[0]
            print("Mostrar los deportes del cliente")

            cur.execute("SELECT * FROM MATRICULAS WHERE ID_CLIENTE = %s", (id,))
            conx.commit()
            matriculas = cur.fetchall()


            if not matriculas:
                print("No hay matriculas")
            else:
                for matricula in matriculas:
                    cur.execute("SELECT * FROM DEPORTES WHERE ID = %s", (matricula[1],))
                    conx.commit()
                    deporte = cur.fetchone()
                    nombre_deporte = deporte[1]


                    matricula = Cliente.Matricula(matricula[0], matricula[1], matricula[2])
                    print(matricula.__deportes__(nombre_deporte))

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de excepción ", error)


while True:
    print("Introduzca 1 para dar de alta a un cliente con sus datos personales")
    print("Introduzca 2 para dar de baja a un cliente")
    print("Introduzca 3 para mostrar los datos de un cliente o de todos")
    print("Introduzca 4 para matricular a un cliente en un deporte")
    print("Introduzca 5 para desmatricular a un cliente de un deporte")
    print("Introduzca 6 para mostrar los deportes de un cliente")
    print("Introduzca 7 para salir")

    opcion = int(input("Introduzca una opción: "))

    if opcion == 1:
        dar_alta_cliente()
    elif opcion == 2:
        dar_baja_cliente()
    elif opcion == 3:
        mostrar_datos_cliente()
    elif opcion == 4:
        matricular_cliente()
    elif opcion == 5:
        borrar_matricula_cliente()
    elif opcion == 6:
        mostrar_deportes_cliente()
    elif opcion == 7:
        if conx is not None:
            conx.close()
        break
    else:
        print("Opción incorrecta")







