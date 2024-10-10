# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class AlumnoDao:

    def getAlumnos(self):

        alumnoSQL = """
        SELECT id, descripcion
        FROM alumnos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(alumnoSQL)
            alumnos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': alumno[0], 'descripcion': alumno[1]} for alumno in alumnos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los alumnos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getAlumnoById(self, id):

        alumnoSQL = """
        SELECT id, descripcion
        FROM alumnos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(alumnoSQL, (id,))
            alumnoEncontrada = cur.fetchone()  # Obtener una sola fila
            if alumnoEncontrada:
                return {
                        "id": alumnoEncontrada[0],
                        "descripcion": alumnoEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra el banco
        except Exception as e:
            app.logger.error(f"Error al obtener alumno {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarAlumno(self, descripcion):

        insertAlumnoSQL = """
        INSERT INTO alumnos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertAlumnoSQL, (descripcion,))
            alumno_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return alumno_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar alumno: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateAlumno(self, id, descripcion):

        updateAlumnoSQL = """
        UPDATE alumnos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateAlumnoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar alumno: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteAlumno(self, id):

        deleteAlumnoSQL = """
        DELETE FROM alumnos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteAlumnoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar alumno: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()   