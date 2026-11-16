
from app.core.database import Database


class ReportesRepository:

    def __init__(self):
        self.db = Database()

    def obtener_reporte_postulaciones(
        self,
        fecha_inicio=None,
        fecha_fin=None,
        estado=None,
        empresa=None
    ):
        conn = None
        cursor = None

        try:
            conn = self.db.get_connection()

            if conn is None:
                raise Exception("No se pudo conectar a la base de datos.")

            cursor = conn.cursor()

            query = """
                SELECT
                    u.nombre AS nombre_estudiante,
                    u.apellido AS apellido_estudiante,
                    e.codigo_estudiantil,
                    e.programa_academico,
                    pp.titulo AS puesto_practica,
                    emp.nombre AS empresa,
                    p.estado,
                    p.fecha_postulacion
                FROM postulaciones p
                INNER JOIN estudiantes e
                    ON p.id_estudiante = e.id_estudiante
                INNER JOIN usuarios u
                    ON u.id_usuario = e.id_estudiante
                INNER JOIN puestos_practica pp
                    ON p.id_puesto = pp.id_puesto
                INNER JOIN empresas emp
                    ON pp.id_empresa = emp.id_empresa
                WHERE 1=1
            """

            parametros = []

            if fecha_inicio:
                query += " AND p.fecha_postulacion >= %s"
                parametros.append(fecha_inicio)

            if fecha_fin:
                query += " AND p.fecha_postulacion < (%s::date + INTERVAL '1 day')"
                parametros.append(fecha_fin)

            if estado:
                query += " AND p.estado = %s"
                parametros.append(estado)

            if empresa:
                query += " AND emp.nombre = %s"
                parametros.append(empresa)

            query += " ORDER BY p.fecha_postulacion DESC"

            cursor.execute(query, tuple(parametros))

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al generar el reporte de postulaciones: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()
