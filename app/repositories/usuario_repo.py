
from app.core.database import Database
from app.models.usuario import Usuario


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
                FROM usuarios
                ORDER BY id_usuario ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener los usuarios: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_por_id(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM usuarios
                WHERE id_usuario = %s
            """, (id_usuario,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener el usuario: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def crear(self, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO usuarios (
                    nombre,
                    apellido,
                    edad,
                    celular,
                    correo,
                    ciudad,
                    contrasena,
                    estado,
                    direccion,
                    id_rol
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario
            """

            cursor.execute(query, (
                usuario.nombre,
                usuario.apellido,
                usuario.edad,
                usuario.celular,
                usuario.correo,
                usuario.ciudad,
                usuario.contraseña,
                usuario.estado,
                usuario.direccion,
                usuario.id_rol
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del usuario creado.")

            nuevo_id = resultado["id_usuario"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Error al crear el usuario: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def eliminar(self, id_usuario: int):
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()
            cursor.execute(
                 """
                 SELECT id_usuario
                 FROM usuarios
                 WHERE id_usuario = %s
                 """,
                 (id_usuario,)
                 )
            usuario = cursor.fetchone()
            
            if usuario is None:
                conn.rollback()
                return False
            cursor.execute(
                """
                  UPDATE empresas
                  SET id_usuario = NULL
                  WHERE id_usuario = %s
                  """,
                  (id_usuario,)
                  )
            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE id_usuario = %s
                RETURNING id_usuario
                """,
                (id_usuario,)
                )
            eliminado = cursor.fetchone()
            conn.commit()
            
            return eliminado is not None
        except Exception as e:
            if conn:
                conn.rollback()
                raise Exception(f"Error al eliminar el usuario: {e}")
            
        finally:
            if cursor:
                cursor.close()
                if conn:
                    conn.close()


    def actualizar(self, id_usuario: int, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE usuarios
                SET
                    nombre = %s,
                    apellido = %s,
                    edad = %s,
                    celular = %s,
                    correo = %s,
                    ciudad = %s,
                    contrasena = %s,
                    estado = %s,
                    direccion = %s,
                    id_rol = %s,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id_usuario = %s
                RETURNING id_usuario
            """

            cursor.execute(query, (
                usuario.nombre,
                usuario.apellido,
                usuario.edad,
                usuario.celular,
                usuario.correo,
                usuario.ciudad,
                usuario.contraseña,
                usuario.estado,
                usuario.direccion,
                usuario.id_rol,
                id_usuario
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Error al actualizar el usuario: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
