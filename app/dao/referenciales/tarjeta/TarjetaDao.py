# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TarjetaDao:

    def getTarjetas(self):

        tarjetaSQL = """
        SELECT id, descripcion
        FROM tarjetas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tarjetaSQL)
            tarjetas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': tarjeta[0], 'descripcion': tarjeta[1]} for tarjeta in tarjetas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas los tarjetas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTarjetaById(self, id):

        tarjetaSQL = """
        SELECT id, descripcion
        FROM tarjetas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tarjetaSQL, (id,))
            tarjetaEncontrada = cur.fetchone()  # Obtener una sola fila
            if tarjetaEncontrada:
                return {
                        "id": tarjetaEncontrada[0],
                        "descripcion": tarjetaEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra la tarjeta
        except Exception as e:
            app.logger.error(f"Error al obtener tarjeta {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTarjeta(self, descripcion):

        insertTarjetaSQL = """
        INSERT INTO tarjetas(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertTarjetaSQL, (descripcion,))
            cargo_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return cargo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar tarjeta: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateTarjeta(self, id, descripcion):

        updateTarjetaSQL = """
        UPDATE tarjetas
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTarjetaSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tarjeta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTarjeta(self, id):

        deleteTarjetaSQL = """
        DELETE FROM tarjetas
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTarjetaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tarjeta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()   