
from app.core.database import Database
from app.models.practicas import Practicas


class PracticasRepository:

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
                FROM practicas
                ORDER BY id_practica ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener las prácticas: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_practica: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM practicas
                WHERE id_practica = %s
            """, (id_practica,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener la práctica: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, practica: Practicas):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO practicas (
                    id_postulacion,
                    id_tutor,
                    fecha_inicio,
                    fecha_fin,
                    horas_requeridas,
                    horas_completadas,
                    objetivo,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_practica
            """

            cursor.execute(query, (
                practica.id_postulacion,
                practica.id_tutor,
                practica.fecha_inicio,
                practica.fecha_fin,
                practica.horas_requeridas,
                practica.horas_completadas,
                practica.objetivo,
                practica.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID de la práctica creada.")

            nuevo_id = resultado["id_practica"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al crear la práctica: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_practica: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_practica
                FROM practicas
                WHERE id_practica = %s
            """, (id_practica,))

            practica = cursor.fetchone()

            if practica is None:
                conn.rollback()
                return False

          
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
                WHERE id_practica = %s
                RETURNING id_practica
            """, (id_practica,))

            eliminado = cursor.fetchone()

            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al eliminar la práctica: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(self, id_practica: int, practica: Practicas):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE practicas
                SET
                    id_postulacion = %s,
                    id_tutor = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    horas_requeridas = %s,
                    horas_completadas = %s,
                    estado = %s,
                    objetivo = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_practica = %s
                RETURNING id_practica
            """

            cursor.execute(query, (
                practica.id_postulacion,
                practica.id_tutor,
                practica.fecha_inicio,
                practica.fecha_fin,
                practica.horas_requeridas,
                practica.horas_completadas,
                practica.estado,
                practica.objetivo,
                id_practica
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al actualizar la práctica: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
