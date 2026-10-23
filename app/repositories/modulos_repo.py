
from app.core.database import Database
from app.models.modulos import Modulos


class ModulosRepository:

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
                FROM modulos
                ORDER BY id_modulo ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener los módulos: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_modulo: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos
                WHERE id_modulo = %s
            """, (id_modulo,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener el módulo: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, modulo: Modulos):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO modulos (
                    nombre,
                    descripcion,
                    estado
                )
                VALUES (%s, %s, %s)
                RETURNING id_modulo
            """

            cursor.execute(query, (
                modulo.nombre,
                modulo.descripcion,
                modulo.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del módulo creado.")

            nuevo_id = resultado["id_modulo"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al crear el módulo: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_modulo: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            # Verificar que el módulo exista.
            cursor.execute("""
                SELECT id_modulo
                FROM modulos
                WHERE id_modulo = %s
            """, (id_modulo,))

            modulo = cursor.fetchone()

            if modulo is None:
                conn.rollback()
                return False

            # Eliminar las relaciones del módulo con los roles.
            cursor.execute("""
                DELETE FROM modulos_x_roles
                WHERE id_modulo = %s
            """, (id_modulo,))

            # Eliminar el módulo.
            cursor.execute("""
                DELETE FROM modulos
                WHERE id_modulo = %s
                RETURNING id_modulo
            """, (id_modulo,))

            eliminado = cursor.fetchone()
            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al eliminar el módulo: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(self, id_modulo: int, modulo: Modulos):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE modulos
                SET
                    nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_modulo = %s
                RETURNING id_modulo
            """

            cursor.execute(query, (
                modulo.nombre,
                modulo.descripcion,
                modulo.estado,
                id_modulo
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(f"Error al actualizar el módulo: {e}")

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
