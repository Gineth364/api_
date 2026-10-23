
from app.core.database import Database
from app.models.seguimiento_practicas import Seguimiento_practicas


class Seguimiento_practicasRepository:

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
                FROM seguimiento_practicas
                ORDER BY id_seguimiento ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al obtener los seguimientos de las practicas: {e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_por_id(self, id_seguimiento: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM seguimiento_practicas
                WHERE id_seguimiento = %s
            """, (id_seguimiento,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(
                f"Error al obtener el seguimiento de la practica: {e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def crear(self, seguimiento_practicas: Seguimiento_practicas):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO seguimiento_practicas (
                    id_practica,
                    fecha_seguimiento,
                    estado,
                    porcentaje_avance,
                    observaciones,
                    dificultades,
                    recomendaciones,
                    fecha_proximo_seguimiento
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_seguimiento
            """

            cursor.execute(query, (
                seguimiento_practicas.id_practica,
                seguimiento_practicas.fecha_seguimiento,
                seguimiento_practicas.estado,
                seguimiento_practicas.porcentaje_avance,
                seguimiento_practicas.observaciones,
                seguimiento_practicas.dificultades,
                seguimiento_practicas.recomendaciones,
                seguimiento_practicas.fecha_proximo_seguimiento
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del seguimiento creado.")

            nuevo_id = resultado["id_seguimiento"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn:
                conn.rollback()

            raise Exception(
                f"Error al crear el seguimiento de la practica: {e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def eliminar(self, id_seguimiento: int):
        conn = None
        cursor = None
        
        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT id_seguimiento
            FROM seguimiento_practicas
            WHERE id_seguimiento = %s
            """, 
            (id_seguimiento,))
            
            seguimiento = cursor.fetchone()
            
            if seguimiento is None:
                conn.rollback()
                return False
            
            cursor.execute("""
            DELETE FROM seguimiento_practicas
            WHERE id_seguimiento = %s
            RETURNING id_seguimiento
            """, 
            (id_seguimiento,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            if conn is not None:
                conn.rollback()
                raise Exception(
                    f"Error al eliminar el seguimiento de la práctica: {e}"
                    )
                
        finally:
            if cursor is not None:
                cursor.close()
                if conn is not None:
                    conn.close()

    def actualizar(
        self,
        id_seguimiento: int,
        seguimiento_practicas: Seguimiento_practicas
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE seguimiento_practicas
                SET
                    id_practica = %s,
                    fecha_seguimiento = %s,
                    estado = %s,
                    porcentaje_avance = %s,
                    observaciones = %s,
                    dificultades = %s,
                    recomendaciones = %s,
                    fecha_proximo_seguimiento = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_seguimiento = %s
                RETURNING id_seguimiento
            """

            cursor.execute(query, (
                seguimiento_practicas.id_practica,
                seguimiento_practicas.fecha_seguimiento,
                seguimiento_practicas.estado,
                seguimiento_practicas.porcentaje_avance,
                seguimiento_practicas.observaciones,
                seguimiento_practicas.dificultades,
                seguimiento_practicas.recomendaciones,
                seguimiento_practicas.fecha_proximo_seguimiento,
                id_seguimiento
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            raise Exception(
                f"Error al actualizar el seguimiento de la practica: {e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
