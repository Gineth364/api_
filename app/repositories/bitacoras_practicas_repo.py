
from app.core.database import Database
from app.models.bitacoras_practicas import Bitacoras_practicas


class BitacorasPracticasRepository:

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
                FROM bitacoras_practica
                ORDER BY id_bitacora ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al obtener las bitácoras de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_bitacora: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM bitacoras_practica
                WHERE id_bitacora = %s
            """, (id_bitacora,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(
                f"Error al obtener la bitácora de práctica: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, bitacora: Bitacoras_practicas):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO bitacoras_practica (
                    id_practica,
                    numero_semana,
                    fecha_inicio,
                    fecha_fin,
                    actividades,
                    logros,
                    dificultades,
                    horas_trabajadas,
                    comentarios_tutor,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_bitacora
            """

            cursor.execute(query, (
                bitacora.id_practica,
                bitacora.numero_semana,
                bitacora.fecha_inicio,
                bitacora.fecha_fin,
                bitacora.actividades,
                bitacora.logros,
                bitacora.dificultades,
                bitacora.horas_trabajadas,
                bitacora.comentarios_tutor,
                bitacora.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception(
                    "No se obtuvo el ID de la bitácora creada."
                )

            nuevo_id = resultado["id_bitacora"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al crear la bitácora de práctica: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_bitacora: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM bitacoras_practica
                WHERE id_bitacora = %s
                RETURNING id_bitacora
            """, (id_bitacora,))

            eliminado = cursor.fetchone()
            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al eliminar la bitácora de práctica: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(
        self,
        id_bitacora: int,
        bitacora: Bitacoras_practicas
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE bitacoras_practica
                SET
                    id_practica = %s,
                    numero_semana = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    actividades = %s,
                    logros = %s,
                    dificultades = %s,
                    horas_trabajadas = %s,
                    comentarios_tutor = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_bitacora = %s
                RETURNING id_bitacora
            """

            cursor.execute(query, (
                bitacora.id_practica,
                bitacora.numero_semana,
                bitacora.fecha_inicio,
                bitacora.fecha_fin,
                bitacora.actividades,
                bitacora.logros,
                bitacora.dificultades,
                bitacora.horas_trabajadas,
                bitacora.comentarios_tutor,
                bitacora.estado,
                id_bitacora
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al actualizar la bitácora de práctica: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
