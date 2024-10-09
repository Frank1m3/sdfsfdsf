# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class SupermercadoDao:

    def getSupermercados(self):

        supermercadoSQL = """
        SELECT id, descripcion
        FROM supermercados
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(supermercadoSQL)
            supermercados = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': supermercado[0], 'descripcion': supermercado[1]} for supermercado in supermercados]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los supermercados: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getSupermercadoById(self, id):

        supermercadoSQL = """
        SELECT id, descripcion
        FROM supermercados WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(supermercadoSQL, (id,))
            supermercadoEncontrada = cur.fetchone()  # Obtener una sola fila
            if supermercadoEncontrada:
                return {
                        "id":supermercadoEncontrada[0],
                        "descripcion": supermercadoEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  
        except Exception as e:
            app.logger.error(f"Error al obtener supermercado {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarSupermercado(self, descripcion):

        insertSupermercadoSQL = """
        INSERT INTO supermercados(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertSupermercadoSQL, (descripcion,))
            supermercado_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return supermercado_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar supermercado: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateSupermercado(self, id, descripcion):

        updateSupermercadoSQL = """
        UPDATE supermercados
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSupermercadoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar supermercado: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteSupermercado(self, id):

        deleteSupermercadoSQL = """
        DELETE FROM supermercados
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteSupermercadoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar supermercado: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()   