# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CarreraDao:

    def getCarreras(self):

        carreraSQL = """
        SELECT id, descripcion
        FROM carreras
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(carreraSQL)
            carreras = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': carrera[0], 'descripcion': carrera[1]} for carrera in carreras]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las carreras: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCarreraById(self, id):

        carreraSQL = """
        SELECT id, descripcion
        FROM carreras WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(carreraSQL, (id,))
            carreraEncontrada = cur.fetchone()  # Obtener una sola fila
            if carreraEncontrada:
                return {
                        "id": carreraEncontrada[0],
                        "descripcion": carreraEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra la carrera
        except Exception as e:
            app.logger.error(f"Error al obtener carrera {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCarrera(self, descripcion):

        insertCarreraSQL = """
        INSERT INTO carreras(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertCarreraSQL, (descripcion,))
            carrera_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return carrera_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar carrera: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateCarrera(self, id, descripcion):

        updateCarreraSQL = """
        UPDATE carreras
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCarreraSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar carrera: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCarrera(self, id):

        deleteCarreraSQL = """
        DELETE FROM carreras
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteCarreraSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar carrera: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
