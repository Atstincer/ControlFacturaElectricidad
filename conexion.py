import pyodbc

class Conexion():

    def __init__(self):

        # Nombre del controlador.
        DRIVER_NAME = "Microsoft Access Driver (*.mdb, *.accdb)"

        # Ruta completa del archivo.
        DB_PATH = r".\BD\ELEC_BD.accdb"

        # user
        UID = "sa"

        # password
        PWD = "DL*2021"

        # Establecer la conexión.
        self.conn = pyodbc.connect("Driver=%s;DBQ=%s;UID=%s;PWD=%s" % (DRIVER_NAME, DB_PATH,UID,PWD))

        # Crear cursor para ejecutar consultas.
        self.cursor = self.conn.cursor()


    def desconectar(self):
        # Cerrar la conexión y, opcionalmente, el cursor antes de finalizar.
        self.cursor.close()
        self.conn.close()


def main():

    obj = Conexion()

    '''
    # Ejecutar consulta: retornar todas las filas de la tabla usuarios.
    q = obj.cursor.execute("SELECT * FROM usuarios")
    rows = q.fetchall()

    # Recorrer cada una de las filas e imprimirlas en pantalla.
    if rows is not None:
        for row in rows:
            print(row)
    else:
        print("No hay datos en la tabla.")
    '''

    obj.desconectar()
        
    print('FIN...')

if __name__ == '__main__':
    main()