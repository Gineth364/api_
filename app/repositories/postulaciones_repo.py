
from app.core.database import Database
from app.models.postulaciones import Postulaciones


class PostulacionesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM postulaciones
                ORDER BY id_postulacion ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener las postulaciones: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_postulacion: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM postulaciones
                WHERE id_postulacion = %s
            """, (id_postulacion,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener la postulación: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, postulacion: Postulaciones):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO postulaciones (
                    id_estudiante,
                    id_puesto,
                    fecha_postulacion,
                    estado,
                    comentarios
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_postulacion
            """

            cursor.execute(query, (
                postulacion.id_estudiante,
                postulacion.id_puesto,
                postulacion.fecha_postulacion,
                postulacion.estado,
                postulacion.comentarios
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception(
                    "No se obtuvo el ID de la postulación creada."
                )

            nuevo_id = resultado["id_postulacion"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al crear la postulación: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_postulacion: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_postulacion
                FROM postulaciones
                WHERE id_postulacion = %s
            """, (id_postulacion,))

            postulacion = cursor.fetchone()

            if postulacion is None:
                conn.rollback()
                return False

            cursor.execute("""
                SELECT id_practica
                FROM practicas
                WHERE id_postulacion = %s
            """, (id_postulacion,))

            practicas = cursor.fetchall()

            for practica in practicas:
                id_practica = practica["id_practica"]

                cursor.execute("""
                    DELETE FROM bitacoras_practica
                    WHERE id_practica = %s
                """, (id_practica,))

                cursor.execute("""
                    DELETE FROM seguimiento_practicas
                    WHERE id_practica = %s
                """, (id_practica,))

                cursor.execute("""
                    DELETE FROM evaluaciones_finales
                    WHERE id_practica = %s
                """, (id_practica,))

       
            cursor.execute("""
                DELETE FROM practicas
                WHERE id_postulacion = %s
            """, (id_postulacion,))

            cursor.execute("""
                DELETE FROM postulaciones
                WHERE id_postulacion = %s
                RETURNING id_postulacion
            """, (id_postulacion,))

            eliminado = cursor.fetchone()
            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al eliminar la postulación: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(self, id_postulacion: int, postulacion: Postulaciones):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE postulaciones
                SET
                    id_estudiante = %s,
                    id_puesto = %s,
                    fecha_postulacion = %s,
                    estado = %s,
                    comentarios = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_postulacion = %s
                RETURNING id_postulacion
            """

            cursor.execute(query, (
                postulacion.id_estudiante,
                postulacion.id_puesto,
                postulacion.fecha_postulacion,
                postulacion.estado,
                postulacion.comentarios,
                id_postulacion
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al actualizar la postulación: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
