# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class BancoDao:

    def getBancos(self):

        bancoSQL = """
        SELECT id, descripcion
        FROM bancos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(bancoSQL)
            bancos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': banco[0], 'descripcion': banco[1]} for banco in bancos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los bancos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getBancoById(self, id):

        bancoSQL = """
        SELECT id, descripcion
        FROM bancos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(bancoSQL, (id,))
            bancoEncontrada = cur.fetchone()  # Obtener una sola fila
            if bancoEncontrada:
                return {
                        "id": bancoEncontrada[0],
                        "descripcion": bancoEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra el banco
        except Exception as e:
            app.logger.error(f"Error al obtener banco {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarBanco(self, descripcion):

        insertBancoSQL = """
        INSERT INTO bancos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertBancoSQL, (descripcion,))
            cargo_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return cargo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar banco: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateBanco(self, id, descripcion):

        updateBancoSQL = """
        UPDATE bancos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateBancoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar banco: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteBanco(self, id):

        deleteBancoSQL = """
        DELETE FROM bancos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteBancoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar banco: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()   