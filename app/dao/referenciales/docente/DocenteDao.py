# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DocenteDao:

    def getDocentes(self):

        docenteSQL = """
        SELECT id, descripcion
        FROM docentes
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(docenteSQL)
            docentes = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': docente[0], 'descripcion': docente[1]} for docente in docentes]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los docentes: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDocenteById(self, id):

        docenteSQL = """
        SELECT id, descripcion
        FROM docentes WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(docenteSQL, (id,))
            docenteEncontrada = cur.fetchone()  # Obtener una sola fila
            if docenteEncontrada:
                return {
                        "id": docenteEncontrada[0],
                        "descripcion": docenteEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra el docente
        except Exception as e:
            app.logger.error(f"Error al obtener docente {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDocente(self, descripcion):

        insertDocenteSQL = """
        INSERT INTO docentes(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDocenteSQL, (descripcion,))
            docente_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return docente_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar docente: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateDocente(self, id, descripcion):

        updateDocenteSQL = """
        UPDATE docentes
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDocenteSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar docente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDocente(self, id):

        deleteDocenteSQL = """
        DELETE FROM docentes
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteDocenteSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar docente: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()   