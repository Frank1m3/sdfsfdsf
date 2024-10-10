# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class VehiculoDao:

    def getVehiculos(self):

        vehiculoSQL = """
        SELECT id, descripcion
        FROM vehiculos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(vehiculoSQL)
            vehiculos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': vehiculo[0], 'descripcion': vehiculo[1]} for vehiculo in vehiculos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los vehiculos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getVehiculoById(self, id):

        vehiculoSQL = """
        SELECT id, descripcion
        FROM vehiculos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(vehiculoSQL, (id,))
            vehiculoEncontrada = cur.fetchone()  # Obtener una sola fila
            if vehiculoEncontrada:
                return {
                        "id": vehiculoEncontrada[0],
                        "descripcion": vehiculoEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra el vehiculo
        except Exception as e:
            app.logger.error(f"Error al obtener vehiculo {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarVehiculo(self, descripcion):

        insertVehiculoSQL = """
        INSERT INTO vehiculos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertVehiculoSQL, (descripcion,))
            vehiculo_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return vehiculo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar vehiculo: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateVehiculo(self, id, descripcion):

        updateVehiculoSQL = """
        UPDATE vehiculos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateVehiculoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar vehiculo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteVehiculo(self, id):

        deleteVehiculoSQL = """
        DELETE FROM vehiculos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteVehiculoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar vehiculo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()   