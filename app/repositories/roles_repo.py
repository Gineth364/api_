
from app.core.database import Database
from app.models.roles import Roles


class RolesRepository:

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
                FROM roles
                ORDER BY id_rol ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener los roles: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_por_id(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM roles
                WHERE id_rol = %s
            """, (id_rol,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener el rol: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def crear(self, roles: Roles):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO roles (
                    nombre,
                    descripcion,
                    estado
                )
                VALUES (%s, %s, %s)
                RETURNING id_rol
            """

            cursor.execute(query, (
                roles.nombre,
                roles.descripcion,
                roles.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del rol creado.")

            nuevo_id = resultado["id_rol"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn:
                conn.rollback()

            raise Exception(f"Error al crear el rol: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def eliminar(self, id_rol: int):
        conn = None
        cursor = None
        
        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()
            
            cursor.execute("""
              SELECT id_rol
              FROM roles
              WHERE id_rol = %s
              """, 
              (id_rol,))
            
            rol = cursor.fetchone()
            
            if rol is None:
                conn.rollback()
                return False
            cursor.execute("""
            DELETE FROM modulos_x_roles
            WHERE id_rol = %s
            """, 
            (id_rol,))

            cursor.execute("""
            UPDATE usuarios
            SET id_rol = NULL
            WHERE id_rol = %s
            """, 
            (id_rol,))
            cursor.execute("""
              DELETE FROM roles
                WHERE id_rol = %s
                RETURNING id_rol
                """, 
                (id_rol,))
            
            eliminado = cursor.fetchone()
            conn.commit()
            
            return eliminado is not None
        except Exception as e:
            if conn is not None:
                conn.rollback()
                
                raise Exception(f"Error al eliminar el rol: {e}")
        finally:
            if cursor is not None:
                cursor.close()
                if conn is not None:
                    conn.close()


    def actualizar(self, id_rol: int, roles: Roles):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE roles
                SET
                    nombre = %s,
                    descripcion = %s,
                    estado = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_rol = %s
                RETURNING id_rol
            """

            cursor.execute(query, (
                roles.nombre,
                roles.descripcion,
                roles.estado,
                id_rol
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            raise Exception(f"Error al actualizar el rol: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
