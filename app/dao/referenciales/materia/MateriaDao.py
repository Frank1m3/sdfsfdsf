# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MateriaDao:

    def getMaterias(self):
        materiaSQL = """
        SELECT id, descripcion
        FROM materias
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(materiaSQL)
            materias = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': materia[0], 'descripcion': materia[1]} for materia in materias]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las materias: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMateriaById(self, id):
        materiaSQL = """
        SELECT id, descripcion
        FROM materias WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(materiaSQL, (id,))
            materiaEncontrada = cur.fetchone()  # Obtener una sola fila
            if materiaEncontrada:
                return {
                    "id": materiaEncontrada[0],
                    "descripcion": materiaEncontrada[1]
                }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra la materia
        except Exception as e:
            app.logger.error(f"Error al obtener materia {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMateria(self, descripcion):
        insertMateriaSQL = """
        INSERT INTO materias(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertMateriaSQL, (descripcion,))
            materia_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return materia_id

        # Si algo fallo entra aquí
        except Exception as e:
            app.logger.error(f"Error al insertar materia: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateMateria(self, id, descripcion):
        updateMateriaSQL = """
        UPDATE materias
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMateriaSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar materia: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMateria(self, id):
        deleteMateriaSQL = """
        DELETE FROM materias
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMateriaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar materia: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
