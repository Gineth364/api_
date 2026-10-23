
from app.core.database import Database
from app.models.empresas import Empresas


class EmpresasRepository:

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
                FROM empresas
                ORDER BY id_empresa ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener las empresas: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_empresa: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM empresas
                WHERE id_empresa = %s
            """, (id_empresa,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener la empresa: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, empresa: Empresas):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO empresas (
                    nombre,
                    identificacion_fiscal,
                    direccion,
                    telefono,
                    correo,
                    persona_contacto,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_empresa
            """

            cursor.execute(query, (
                empresa.nombre,
                empresa.identificacion_fiscal,
                empresa.direccion,
                empresa.telefono,
                empresa.correo,
                empresa.persona_contacto,
                empresa.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID de la empresa creada.")

            nuevo_id = resultado["id_empresa"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al crear la empresa: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_empresa: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT id_empresa
                FROM empresas
                WHERE id_empresa = %s
            """, (id_empresa,))

            empresa = cursor.fetchone()

            if empresa is None:
                conn.rollback()
                return False
            
            cursor.execute("""
                SELECT id_puesto
                FROM puestos_practica
                WHERE id_empresa = %s
            """, (id_empresa,))

            puestos = cursor.fetchall()

            for puesto in puestos:
                id_puesto = puesto["id_puesto"]

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
                WHERE id_empresa = %s
            """, (id_empresa,))

            cursor.execute("""
                UPDATE empresas
                SET id_usuario = NULL
                WHERE id_empresa = %s
            """, (id_empresa,))

      
            cursor.execute("""
                DELETE FROM empresas
                WHERE id_empresa = %s
                RETURNING id_empresa
            """, (id_empresa,))

            eliminado = cursor.fetchone()
            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al eliminar la empresa: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(self, id_empresa: int, empresa: Empresas):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE empresas
                SET
                    nombre = %s,
                    identificacion_fiscal = %s,
                    direccion = %s,
                    telefono = %s,
                    correo = %s,
                    persona_contacto = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_empresa = %s
                RETURNING id_empresa
            """

            cursor.execute(query, (
                empresa.nombre,
                empresa.identificacion_fiscal,
                empresa.direccion,
                empresa.telefono,
                empresa.correo,
                empresa.persona_contacto,
                empresa.estado,
                id_empresa
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al actualizar la empresa: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
