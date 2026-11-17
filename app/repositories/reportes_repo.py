
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

from app.core.database import Database


class ReportesRepository:

    def __init__(self):
        self.db = Database()

    # ==========================================
    # REPORTE DE POSTULACIONES
    # ==========================================

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
                query += """
                    AND p.fecha_postulacion <
                    (%s::date + INTERVAL '1 day')
                """
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

    # ==========================================
    # REPORTE DE PRACTICAS
    # ==========================================

    def obtener_reporte_practicas(
        self,
        fecha_inicio=None,
        fecha_fin=None,
        estado=None,
        empresa=None,
        tutor=None
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
                    ue.nombre AS nombre_estudiante,
                    ue.apellido AS apellido_estudiante,
                    e.codigo_estudiantil,
                    e.programa_academico,
                    emp.nombre AS empresa,
                    pp.titulo AS puesto_practica,
                    ut.nombre AS nombre_tutor,
                    ut.apellido AS apellido_tutor,
                    pr.fecha_inicio,
                    pr.fecha_fin,
                    pr.horas_requeridas,
                    pr.horas_completadas,
                    pr.objetivo,
                    pr.estado
                FROM practicas pr

                INNER JOIN postulaciones po
                    ON pr.id_postulacion = po.id_postulacion

                INNER JOIN estudiantes e
                    ON po.id_estudiante = e.id_estudiante

                INNER JOIN usuarios ue
                    ON ue.id_usuario = e.id_estudiante

                INNER JOIN puestos_practica pp
                    ON po.id_puesto = pp.id_puesto

                INNER JOIN empresas emp
                    ON pp.id_empresa = emp.id_empresa

                INNER JOIN tutores t
                    ON pr.id_tutor = t.id_tutor

                INNER JOIN usuarios ut
                    ON ut.id_usuario = t.id_tutor

                WHERE 1=1
            """

            parametros = []

            # Filtrar prácticas que coincidan con el período
            if fecha_inicio:
                query += " AND pr.fecha_fin >= %s"
                parametros.append(fecha_inicio)

            if fecha_fin:
                query += " AND pr.fecha_inicio <= %s"
                parametros.append(fecha_fin)

            if estado:
                query += " AND pr.estado = %s"
                parametros.append(estado)

            if empresa:
                query += " AND emp.nombre = %s"
                parametros.append(empresa)

            if tutor:
                query += """
                    AND (
                        ut.nombre || ' ' || COALESCE(ut.apellido, '')
                    ) ILIKE %s
                """
                parametros.append(f"%{tutor}%")

            query += " ORDER BY pr.fecha_inicio DESC"

            cursor.execute(query, tuple(parametros))

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al generar el reporte de prácticas: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()

    # ==========================================
    # REPORTE DE EVALUACIONES FINALES
    # ==========================================

    def obtener_reporte_evaluaciones(
        self,
        fecha_inicio=None,
        fecha_fin=None,
        estado=None,
        empresa=None,
        tipo_evaluacion=None
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
                    ue.nombre AS nombre_estudiante,
                    ue.apellido AS apellido_estudiante,
                    e.codigo_estudiantil,
                    e.programa_academico,

                    emp.nombre AS empresa,
                    pp.titulo AS puesto_practica,

                    ut.nombre AS nombre_tutor,
                    ut.apellido AS apellido_tutor,

                    COALESCE(ev.nombre, 'Sin asignar')
                        AS nombre_evaluador,
                    COALESCE(ev.apellido, '')
                        AS apellido_evaluador,

                    ef.tipo_evaluacion,
                    ef.fecha_evaluacion,
                    ef.resultado,
                    ef.calificacion,
                    ef.cumplimiento_objetivos,
                    ef.desempeno,
                    ef.fortalezas,
                    ef.aspectos_mejora,
                    ef.observaciones,
                    ef.recomendaciones,
                    ef.estado

                FROM evaluaciones_finales ef

                INNER JOIN practicas pr
                    ON ef.id_practica = pr.id_practica

                INNER JOIN postulaciones po
                    ON pr.id_postulacion = po.id_postulacion

                INNER JOIN estudiantes e
                    ON po.id_estudiante = e.id_estudiante

                INNER JOIN usuarios ue
                    ON ue.id_usuario = e.id_estudiante

                INNER JOIN puestos_practica pp
                    ON po.id_puesto = pp.id_puesto

                INNER JOIN empresas emp
                    ON pp.id_empresa = emp.id_empresa

                INNER JOIN tutores t
                    ON pr.id_tutor = t.id_tutor

                INNER JOIN usuarios ut
                    ON ut.id_usuario = t.id_tutor

                LEFT JOIN usuarios ev
                    ON ev.id_usuario = ef.id_evaluador

                WHERE 1=1
            """

            parametros = []

            if fecha_inicio:
                query += " AND ef.fecha_evaluacion >= %s"
                parametros.append(fecha_inicio)

            if fecha_fin:
                query += """
                    AND ef.fecha_evaluacion <
                    (%s::date + INTERVAL '1 day')
                """
                parametros.append(fecha_fin)

            if estado:
                query += " AND ef.estado = %s"
                parametros.append(estado)

            if empresa:
                query += " AND emp.nombre = %s"
                parametros.append(empresa)

            if tipo_evaluacion:
                query += " AND ef.tipo_evaluacion = %s"
                parametros.append(tipo_evaluacion)

            query += " ORDER BY ef.fecha_evaluacion DESC"

            cursor.execute(query, tuple(parametros))

            return cursor.fetchall()

        except Exception as e:
            raise Exception(
                f"Error al generar el reporte de evaluaciones: {e}"
            )

        finally:
            if cursor is not None:
                cursor.close()

            if conn is not None:
                conn.close()
