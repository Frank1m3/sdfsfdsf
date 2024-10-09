# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MarcaDao:

    def getMarcas(self):

        marcaSQL = """
        SELECT id, descripcion
        FROM marcas
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(marcaSQL)
            marcas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': marca[0], 'descripcion': marca[1]} for marca in marcas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las marcas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMarcaById(self, id):

        marcaSQL = """
        SELECT id, descripcion
        FROM marcas WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(marcaSQL, (id,))
            marcaEncontrada = cur.fetchone()  # Obtener una sola fila
            if marcaEncontrada:
                return {
                        "id": marcaEncontrada[0],
                        "descripcion": marcaEncontrada[1]
                    }  # Retornar los datos de la marca
            else:
                return None  # Retornar None si no se encuentra la marca
        except Exception as e:
            app.logger.error(f"Error al obtener marca: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMarca(self, descripcion):

        insertMarcaSQL = """
        INSERT INTO marcas(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertMarcaSQL, (descripcion,))
            marca_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return marca_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar marca: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateMarca(self, id, descripcion):

        updateMarcaSQL = """
        UPDATE marcas
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMarcaSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar marca: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMarca(self, id):

        deleteMarcaSQL = """
        DELETE FROM marcas
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMarcaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar marca: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
