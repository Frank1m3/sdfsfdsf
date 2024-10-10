# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EntidadDao:

    def getEntidades(self):
        entidadSQL = """
        SELECT id, descripcion
        FROM entidades
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(entidadSQL)
            entidades = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': entidad[0], 'descripcion': entidad[1]} for entidad in entidades]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las entidades: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEntidadById(self, id):
        entidadSQL = """
        SELECT id, descripcion
        FROM entidades WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(entidadSQL, (id,))
            entidadEncontrada = cur.fetchone()  # Obtener una sola fila
            if entidadEncontrada:
                return {
                    "id": entidadEncontrada[0],
                    "descripcion": entidadEncontrada[1]
                }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra la entidad
        except Exception as e:
            app.logger.error(f"Error al obtener entidad: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEntidad(self, descripcion):
        insertEntidadSQL = """
        INSERT INTO entidades(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEntidadSQL, (descripcion,))
            entidad_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return entidad_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar entidad: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEntidad(self, id, descripcion):
        updateEntidadSQL = """
        UPDATE entidades
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEntidadSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar entidad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEntidad(self, id):
        deleteEntidadSQL = """
        DELETE FROM entidades
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteEntidadSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar entidad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
