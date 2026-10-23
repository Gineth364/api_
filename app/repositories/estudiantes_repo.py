
from app.core.database import Database
from app.models.estudiantes import Usuario


class UsuarioRepository:

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
                FROM estudiantes
                ORDER BY id_estudiante ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener los estudiantes: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_estudiante: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM estudiantes
                WHERE id_estudiante = %s
            """, (id_estudiante,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener el estudiante: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, estudiante: Usuario):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            if estudiante.id_estudiante is None:
                raise Exception(
                    "Debes proporcionar el ID de un usuario existente "
                    "para registrarlo como estudiante."
                )

            query = """
                INSERT INTO estudiantes (
                    id_estudiante,
                    codigo_estudiantil,
                    programa_academico,
                    semestre,
                    estado_academico
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_estudiante
            """

            cursor.execute(query, (
                estudiante.id_estudiante,
                estudiante.codigo_estudiantil,
                estudiante.programa_academico,
                estudiante.semestre,
                estudiante.estado_academico
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del estudiante creado.")

            nuevo_id = resultado["id_estudiante"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al crear el estudiante: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_estudiante: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_estudiante
                FROM estudiantes
                WHERE id_estudiante = %s
            """, (id_estudiante,))

            estudiante = cursor.fetchone()

            if estudiante is None:
                conn.rollback()
                return False

            cursor.execute("""
                SELECT id_postulacion
                FROM postulaciones
                WHERE id_estudiante = %s
            """, (id_estudiante,))

            postulaciones = cursor.fetchall()

            for postulacion in postulaciones:
                id_postulacion = postulacion["id_postulacion"]

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
                WHERE id_estudiante = %s
            """, (id_estudiante,))

            cursor.execute("""
                DELETE FROM estudiantes
                WHERE id_estudiante = %s
                RETURNING id_estudiante
            """, (id_estudiante,))

            eliminado = cursor.fetchone()

            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al eliminar el estudiante: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(self, id_estudiante: int, estudiante: Usuario):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE estudiantes
                SET
                    codigo_estudiantil = %s,
                    programa_academico = %s,
                    semestre = %s,
                    estado_academico = %s
                WHERE id_estudiante = %s
                RETURNING id_estudiante
            """

            cursor.execute(query, (
                estudiante.codigo_estudiantil,
                estudiante.programa_academico,
                estudiante.semestre,
                estudiante.estado_academico,
                id_estudiante
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al actualizar el estudiante: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
