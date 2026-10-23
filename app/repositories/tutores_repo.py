
from app.core.database import Database
from app.models.tutores import Usuario


class TutoresRepository:

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
                FROM tutores
                ORDER BY id_tutor ASC
            """)

            return cursor.fetchall()

        except Exception as e:
            raise Exception(f"Error al obtener los tutores: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_por_id(self, id_tutor: int):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM tutores
                WHERE id_tutor = %s
            """, (id_tutor,))

            return cursor.fetchone()

        except Exception as e:
            raise Exception(f"Error al obtener el tutor: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def crear(self, tutor: Usuario):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                INSERT INTO tutores (
                    id_tutor,
                    especialidad,
                    cargo,
                    estado
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_tutor
            """

            cursor.execute(query, (
                tutor.id_tutor,
                tutor.especialidad,
                tutor.cargo,
                tutor.estado
            ))

            resultado = cursor.fetchone()

            if resultado is None:
                raise Exception("No se obtuvo el ID del tutor creado.")

            nuevo_id = resultado["id_tutor"]
            conn.commit()

            return nuevo_id

        except Exception as e:
            if conn:
                conn.rollback()

            raise Exception(f"Error al crear el tutor: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def eliminar(self, id_tutor: int):
        conn = None
        cursor = None
        
        try:
            conn = self.db.get_connection()
            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT id_tutor
            FROM tutores
            WHERE id_tutor = %s
            """, 
            (id_tutor,))
            tutor = cursor.fetchone()
            
            if tutor is None:
                conn.rollback()
                return False
            
            cursor.execute("""
            SELECT id_practica
            FROM practicas
            WHERE id_tutor = %s
            """, 
            (id_tutor,))
            
            practicas = cursor.fetchall()
            for practica in practicas:
                
                id_practica = practica["id_practica"]
                cursor.execute("""
                DELETE FROM bitacoras_practica
                WHERE id_practica = %s
                """, 
                (id_practica,))
                
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
                  WHERE id_tutor = %s
                  """, (id_tutor,))
                cursor.execute("""
                DELETE FROM tutores
                WHERE id_tutor = %s
                RETURNING id_tutor
                """, (id_tutor,))
                
                eliminado = cursor.fetchone()
                conn.commit()
                return eliminado is not None
        except Exception as e:
            if conn is not None:
                conn.rollback()
                raise Exception(f"Error al eliminar el tutor: {e}")
            
        finally:
            if cursor is not None:
                cursor.close()
                if conn is not None:
                    conn.close()


    def actualizar(self, id_tutor: int, tutor: Usuario):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                UPDATE tutores
                SET
                    especialidad = %s,
                    cargo = %s,
                    estado = %s
                WHERE id_tutor = %s
                RETURNING id_tutor
            """

            cursor.execute(query, (
                tutor.especialidad,
                tutor.cargo,
                tutor.estado,
                id_tutor
            ))

            actualizado = cursor.fetchone()
            conn.commit()

            return actualizado is not None

        except Exception as e:
            if conn:
                conn.rollback()

            raise Exception(f"Error al actualizar el tutor: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
