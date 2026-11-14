
from app.core.database import Database
from app.models.evaluaciones_finales import EvaluacionesFinales


class EvaluacionesFinalesRepository:

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
                FROM evaluaciones_finales
                ORDER BY id_evaluacion ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al obtener las evaluaciones finales: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_evaluacion: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM evaluaciones_finales
                WHERE id_evaluacion = %s
            """, (id_evaluacion,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(
                f"Error al obtener la evaluación final: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, evaluaciones_finales: EvaluacionesFinales):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO evaluaciones_finales (
                    id_practica,
                    id_evaluador,
                    tipo_evaluacion,
                    fecha_evaluacion,
                    resultado,
                    calificacion,
                    cumplimiento_objetivos,
                    desempeno,
                    fortalezas,
                    aspectos_mejora,
                    observaciones,
                    recomendaciones,
                    estado
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                RETURNING id_evaluacion
            """

            cursor.execute(query, (
                evaluaciones_finales.id_practica,
                evaluaciones_finales.id_evaluador,
                evaluaciones_finales.tipo_evaluacion,
                evaluaciones_finales.fecha_evaluacion,
                evaluaciones_finales.resultado,
                evaluaciones_finales.calificacion,
                evaluaciones_finales.cumplimiento_objetivos,
                evaluaciones_finales.desempeno,
                evaluaciones_finales.fortalezas,
                evaluaciones_finales.aspectos_mejora,
                evaluaciones_finales.observaciones,
                evaluaciones_finales.recomendaciones,
                evaluaciones_finales.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception(
                    "No se obtuvo el ID de la evaluación creada."
                )

            nuevo_id = resultado["id_evaluacion"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al crear la evaluación final: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_evaluacion: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_evaluacion
                FROM evaluaciones_finales
                WHERE id_evaluacion = %s
            """, (id_evaluacion,))

            evaluacion = cursor.fetchone()

            if evaluacion is None:
                conn.rollback()
                return False

            cursor.execute("""
                DELETE FROM evaluaciones_finales
                WHERE id_evaluacion = %s
                RETURNING id_evaluacion
            """, (id_evaluacion,))

            eliminado = cursor.fetchone()
            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al eliminar la evaluación final: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(
        self,
        id_evaluacion: int,
        evaluaciones_finales: EvaluacionesFinales
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE evaluaciones_finales
                SET
                    id_practica = %s,
                    id_evaluador = %s,
                    tipo_evaluacion = %s,
                    fecha_evaluacion = %s,
                    resultado = %s,
                    calificacion = %s,
                    cumplimiento_objetivos = %s,
                    desempeno = %s,
                    fortalezas = %s,
                    aspectos_mejora = %s,
                    observaciones = %s,
                    recomendaciones = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_evaluacion = %s
                RETURNING id_evaluacion
            """

            cursor.execute(query, (
                evaluaciones_finales.id_practica,
                evaluaciones_finales.id_evaluador,
                evaluaciones_finales.tipo_evaluacion,
                evaluaciones_finales.fecha_evaluacion,
                evaluaciones_finales.resultado,
                evaluaciones_finales.calificacion,
                evaluaciones_finales.cumplimiento_objetivos,
                evaluaciones_finales.desempeno,
                evaluaciones_finales.fortalezas,
                evaluaciones_finales.aspectos_mejora,
                evaluaciones_finales.observaciones,
                evaluaciones_finales.recomendaciones,
                evaluaciones_finales.estado,
                id_evaluacion
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al actualizar la evaluación final: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
