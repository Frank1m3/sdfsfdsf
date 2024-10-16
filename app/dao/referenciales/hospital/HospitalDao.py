# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class HospitalDao:

    def getHospitales(self):

        hospitalSQL = """
        SELECT id, descripcion
        FROM hospitales
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(hospitalSQL)
            hospitales = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': hospital[0], 'descripcion': hospital[1]} for hospital in hospitales]

        except Exception as e:
            app.logger.error(f"Error al obtener todas los hospitales: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getHospitalById(self, id):

        hospitalSQL = """
        SELECT id, descripcion
        FROM hospitales WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(hospitalSQL, (id,))
            hospitalEncontrada = cur.fetchone()  # Obtener una sola fila
            if hospitalEncontrada:
                return {
                        "id": hospitalEncontrada[0],
                        "descripcion": hospitalEncontrada[1]
                    }  # Retornar los datos
            else:
                return None  # Retornar None si no se encuentra cargo
        except Exception as e:
            app.logger.error(f"Error al obtener hospital {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarHospital(self, descripcion):

        insertHospitalSQL = """
        INSERT INTO hospitales(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertHospitalSQL, (descripcion,))
            hospital_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return hospital_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar hospital: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateHospital(self, id, descripcion):

        updateHospitalSQL = """
        UPDATE hospitales
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateHospitalSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar hospital: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteHospital(self, id):

        deleteHospitalSQL = """
        DELETE FROM hospitales
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteHospitalSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar hospital: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()