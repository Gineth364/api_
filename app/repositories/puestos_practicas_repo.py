
from app.core.database import Database
from app.models.puestos_practicas import Puestos_practica


class Puestos_practicasRepository:

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
                FROM puestos_practica
                ORDER BY id_puesto ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al obtener los puestos de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_puesto: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM puestos_practica
                WHERE id_puesto = %s
            """, (id_puesto,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(
                f"Error al obtener el puesto de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, puestos_practica: Puestos_practica):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO puestos_practica (
                    id_empresa,
                    titulo,
                    descripcion,
                    requisitos,
                    area,
                    modalidad,
                    fecha_inicio,
                    fecha_fin,
                    cupos_disponibles,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_puesto
            """

            cursor.execute(query, (
                puestos_practica.id_empresa,
                puestos_practica.titulo,
                puestos_practica.descripcion,
                puestos_practica.requisitos,
                puestos_practica.area,
                puestos_practica.modalidad,
                puestos_practica.fecha_inicio,
                puestos_practica.fecha_fin,
                puestos_practica.cupos_disponibles,
                puestos_practica.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del puesto creado.")

            nuevo_id = resultado["id_puesto"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al crear el puesto de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_puesto: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_puesto
                FROM puestos_practica
                WHERE id_puesto = %s
            """, (id_puesto,))

            puesto = cursor.fetchone()

            if puesto is None:
                conn.rollback()
                return False

            cursor.execute("""
                SELECT id_postulacion
                FROM postulaciones
                WHERE id_puesto = %s
            """, (id_puesto,))

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
                WHERE id_puesto = %s
            """, (id_puesto,))

            cursor.execute("""
                DELETE FROM puestos_practica
                WHERE id_puesto = %s
                RETURNING id_puesto
            """, (id_puesto,))

            eliminado = cursor.fetchone()

            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al eliminar el puesto de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(
        self,
        id_puesto: int,
        puestos_practica: Puestos_practica
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE puestos_practica
                SET
                    titulo = %s,
                    descripcion = %s,
                    requisitos = %s,
                    area = %s,
                    modalidad = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    cupos_disponibles = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_puesto = %s
                RETURNING id_puesto
            """

            cursor.execute(query, (
                puestos_practica.titulo,
                puestos_practica.descripcion,
                puestos_practica.requisitos,
                puestos_practica.area,
                puestos_practica.modalidad,
                puestos_practica.fecha_inicio,
                puestos_practica.fecha_fin,
                puestos_practica.cupos_disponibles,
                puestos_practica.estado,
                id_puesto
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al actualizar el puesto de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
