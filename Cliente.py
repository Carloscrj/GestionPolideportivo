class Cliente:
    def __init__(self, nombre, apellidos, dni, fecha_nacimiento, telefono):
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono

    def __str__(self):
        return "Nombre: " + self.nombre + " Apellidos:" + self.apellidos + " DNI: " + self.dni + " Fecha de nacimiento: " + self.fecha_nacimiento + " Teléfono: " + self.telefono

    def __datos__(self):
        return self.nombre, self.apellidos, self.dni, self.fecha_nacimiento, self.telefono


class Matricula:
    def __init__(self, id_cliente, id_deporte, precio):
        self.id_cliente = id_cliente
        self.id_deporte = id_deporte
        self.precio = precio

    def __str__(self):
        return "Id cliente: " + str(self.id_cliente) + "Id deporte: " + str(self.id_deporte) + "Precio: " + str(self.precio)

    def __deportes__(self, nombre_deporte):
        return "-Id cliente: " + str(self.id_cliente) + " -Id deporte: " + str(self.id_deporte) + " -Precio: " + str(self.precio) + " -Nombre del deporte: " + nombre_deporte


