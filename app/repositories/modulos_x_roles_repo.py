
from app.core.database import Database
from app.models.modulos_x_roles import Modulos_x_roles


class Modulos_x_rolesRepository:

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
                FROM modulos_x_roles
                ORDER BY id_modulo_rol ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al obtener los módulos por rol: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def obtener_por_id(self, id_modulo_rol: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM modulos_x_roles
                WHERE id_modulo_rol = %s
            """, (id_modulo_rol,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(
                f"Error al obtener la relación módulo-rol: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def crear(self, modulos_x_roles: Modulos_x_roles):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO modulos_x_roles (
                    id_modulo,
                    id_rol,
                    puede_ver,
                    puede_crear,
                    puede_actualizar,
                    puede_eliminar,
                    estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_modulo_rol
            """

            cursor.execute(query, (
                modulos_x_roles.id_modulo,
                modulos_x_roles.id_rol,
                modulos_x_roles.puede_ver,
                modulos_x_roles.puede_crear,
                modulos_x_roles.puede_actualizar,
                modulos_x_roles.puede_eliminar,
                modulos_x_roles.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception(
                    "No se obtuvo el ID de la relación creada."
                )

            nuevo_id = resultado["id_modulo_rol"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al crear la relación módulo-rol: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def eliminar(self, id_modulo_rol: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

        
            cursor.execute("""
                SELECT id_modulo_rol
                FROM modulos_x_roles
                WHERE id_modulo_rol = %s
            """, (id_modulo_rol,))

            relacion = cursor.fetchone()

            if relacion is None:
                conn.rollback()
                return False

            cursor.execute("""
                DELETE FROM modulos_x_roles
                WHERE id_modulo_rol = %s
                RETURNING id_modulo_rol
            """, (id_modulo_rol,))

            eliminado = cursor.fetchone()
            conn.commit()

            return eliminado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al eliminar la relación módulo-rol: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def actualizar(
        self,
        id_modulo_rol: int,
        modulos_x_roles: Modulos_x_roles
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE modulos_x_roles
                SET
                    id_modulo = %s,
                    id_rol = %s,
                    puede_ver = %s,
                    puede_crear = %s,
                    puede_actualizar = %s,
                    puede_eliminar = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_modulo_rol = %s
                RETURNING id_modulo_rol
            """

            cursor.execute(query, (
                modulos_x_roles.id_modulo,
                modulos_x_roles.id_rol,
                modulos_x_roles.puede_ver,
                modulos_x_roles.puede_crear,
                modulos_x_roles.puede_actualizar,
                modulos_x_roles.puede_eliminar,
                modulos_x_roles.estado,
                id_modulo_rol
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn is not None:
                conn.rollback()

            raise Exception(
                f"Error al actualizar la relación módulo-rol: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
