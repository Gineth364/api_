
from io import BytesIO
from datetime import datetime, date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A3
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)
from openpyxl.utils import get_column_letter


# ==========================================
# CONFIGURACIÓN INSTITUCIONAL
# ==========================================

AZUL = "173B67"
AZUL_CLARO = "DCEAF7"
BLANCO = "FFFFFF"
GRIS = "52657A"
BORDE = "D5DFEA"


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def formatear_fecha(valor):

    if valor is None:
        return ""

    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M")

    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")

    return str(valor)


def texto_seguro(valor):

    if valor is None:
        return ""

    return escape(str(valor))


def obtener_valor(fila, campo):

    valor = fila.get(campo)

    if valor is None:
        return ""

    if isinstance(valor, (datetime, date)):
        return formatear_fecha(valor)

    return str(valor)


def obtener_estudiante(fila):

    nombre = fila.get("nombre_estudiante") or ""
    apellido = fila.get("apellido_estudiante") or ""

    return f"{nombre} {apellido}".strip()


def obtener_tutor(fila):

    nombre = fila.get("nombre_tutor") or ""
    apellido = fila.get("apellido_tutor") or ""

    return f"{nombre} {apellido}".strip()


def obtener_evaluador(fila):

    nombre = fila.get("nombre_evaluador") or ""
    apellido = fila.get("apellido_evaluador") or ""

    return f"{nombre} {apellido}".strip()


# ==========================================
# GENERADOR GENERAL DE PDF
# ==========================================

def generar_pdf_general(datos, titulo_reporte, columnas):

    archivo = BytesIO()

    documento = SimpleDocTemplate(
        archivo,
        pagesize=landscape(A3),
        rightMargin=25,
        leftMargin=25,
        topMargin=30,
        bottomMargin=30
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloInstitucional",
        parent=estilos["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=colors.HexColor("#173B67"),
        alignment=TA_CENTER,
        spaceAfter=5
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#52657A"),
        alignment=TA_CENTER
    )

    encabezado = ParagraphStyle(
        "EncabezadoTabla",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    contenido = ParagraphStyle(
        "ContenidoTabla",
        parent=estilos["Normal"],
        fontSize=6.5,
        leading=8,
        alignment=TA_LEFT,
        wordWrap="CJK"
    )

    elementos = []

    elementos.append(
        Paragraph("UniPrácticas", titulo)
    )

    elementos.append(
        Paragraph(
            "Sistema de Seguimiento de Prácticas Profesionales",
            subtitulo
        )
    )

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            f"<b>{texto_seguro(titulo_reporte)}</b>",
            ParagraphStyle(
                "Reporte",
                parent=estilos["Heading2"],
                textColor=colors.HexColor("#173B67"),
                alignment=TA_CENTER
            )
        )
    )

    elementos.append(
        Paragraph(
            f"Fecha de generación: "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Total de registros: {len(datos)}",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 12))

    tabla_datos = [
        [
            Paragraph(texto_seguro(columna["titulo"]), encabezado)
            for columna in columnas
        ]
    ]

    for fila in datos:

        fila_pdf = []

        for columna in columnas:

            if columna.get("campo") == "__estudiante__":
                valor = obtener_estudiante(fila)

            elif columna.get("campo") == "__tutor__":
                valor = obtener_tutor(fila)

            elif columna.get("campo") == "__evaluador__":
                valor = obtener_evaluador(fila)

            else:
                valor = obtener_valor(fila, columna["campo"])

            fila_pdf.append(
                Paragraph(texto_seguro(valor), contenido)
            )

        tabla_datos.append(fila_pdf)

    ancho_disponible = landscape(A3)[0] - 50

    proporciones = [
        columna.get("peso", 1)
        for columna in columnas
    ]

    suma_proporciones = sum(proporciones)

    anchos = [
        ancho_disponible * peso / suma_proporciones
        for peso in proporciones
    ]

    tabla = Table(
        tabla_datos,
        colWidths=anchos,
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173B67")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DFEA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#EEF4FA")
        ])
    ]))

    elementos.append(tabla)

    def pie_pagina(canvas, documento):

        canvas.saveState()

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#52657A"))

        canvas.drawString(
            25,
            18,
            f"UniPrácticas | {titulo_reporte}"
        )

        canvas.drawRightString(
            documento.pagesize[0] - 25,
            18,
            f"Página {documento.page}"
        )

        canvas.restoreState()

    documento.build(
        elementos,
        onFirstPage=pie_pagina,
        onLaterPages=pie_pagina
    )

    archivo.seek(0)

    return archivo


# ==========================================
# GENERADOR GENERAL DE EXCEL
# ==========================================

def generar_excel_general(datos, nombre_hoja, titulo_reporte, columnas):

    libro = Workbook()
    hoja = libro.active

    hoja.title = nombre_hoja

    cantidad_columnas = len(columnas)

    ultima_columna = get_column_letter(cantidad_columnas)

    # ENCABEZADO INSTITUCIONAL

    hoja.merge_cells(f"A1:{ultima_columna}1")
    hoja["A1"] = "UniPrácticas"

    hoja["A1"].font = Font(
        name="Arial",
        size=18,
        bold=True,
        color=BLANCO
    )

    hoja["A1"].fill = PatternFill(
        fill_type="solid",
        fgColor=AZUL
    )

    hoja["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    hoja.row_dimensions[1].height = 32

    hoja.merge_cells(f"A2:{ultima_columna}2")

    hoja["A2"] = (
        "Sistema de Seguimiento de Prácticas Profesionales"
    )

    hoja["A2"].font = Font(
        name="Arial",
        size=10,
        italic=True,
        color=AZUL
    )

    hoja["A2"].alignment = Alignment(
        horizontal="center"
    )

    # TÍTULO DEL REPORTE

    hoja.merge_cells(f"A4:{ultima_columna}4")
    hoja["A4"] = titulo_reporte

    hoja["A4"].font = Font(
        size=14,
        bold=True,
        color=AZUL
    )

    hoja["A4"].alignment = Alignment(
        horizontal="center"
    )

    # INFORMACIÓN GENERAL

    hoja["A5"] = "Fecha de generación:"
    hoja["B5"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    hoja["A6"] = "Total de registros:"
    hoja["B6"] = len(datos)

    hoja["A5"].font = Font(bold=True, color=AZUL)
    hoja["A6"].font = Font(bold=True, color=AZUL)

    # ENCABEZADOS

    fila_encabezado = 8

    for numero_columna, columna in enumerate(columnas, start=1):

        celda = hoja.cell(
            row=fila_encabezado,
            column=numero_columna,
            value=columna["titulo"]
        )

        celda.font = Font(
            bold=True,
            color=BLANCO
        )

        celda.fill = PatternFill(
            fill_type="solid",
            fgColor=AZUL
        )

        celda.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    hoja.row_dimensions[fila_encabezado].height = 35

    # REGISTROS

    for numero_fila, fila in enumerate(datos, start=9):

        for numero_columna, columna in enumerate(columnas, start=1):

            if columna.get("campo") == "__estudiante__":
                valor = obtener_estudiante(fila)

            elif columna.get("campo") == "__tutor__":
                valor = obtener_tutor(fila)

            elif columna.get("campo") == "__evaluador__":
                valor = obtener_evaluador(fila)

            else:
                valor = fila.get(columna["campo"])

            if isinstance(valor, datetime) and valor.tzinfo:
                valor = valor.replace(tzinfo=None)

            if valor is not None and not isinstance(
                valor,
                (str, int, float, bool, datetime, date)
            ):
                valor = str(valor)

            celda = hoja.cell(
                row=numero_fila,
                column=numero_columna,
                value=valor
            )

            celda.fill = PatternFill(
                fill_type="solid",
                fgColor=BLANCO if numero_fila % 2 else AZUL_CLARO
            )

            celda.alignment = Alignment(
                vertical="center",
                wrap_text=True
            )

            celda.border = Border(
                bottom=Side(
                    style="thin",
                    color=BORDE
                )
            )

            if isinstance(valor, (datetime, date)):
                celda.number_format = (
                    "dd/mm/yyyy hh:mm"
                    if isinstance(valor, datetime)
                    else "dd/mm/yyyy"
                )

    # ANCHOS DE COLUMNAS

    for numero_columna, columna in enumerate(columnas, start=1):

        hoja.column_dimensions[
            get_column_letter(numero_columna)
        ].width = columna.get("ancho", 22)

    # PRESENTACIÓN

    hoja.freeze_panes = "A9"

    hoja.auto_filter.ref = (
        f"A8:{ultima_columna}{max(8, len(datos) + 8)}"
    )

    hoja.sheet_view.showGridLines = False

    hoja.oddFooter.center.text = (
        f"UniPrácticas | {titulo_reporte}"
    )

    hoja.oddFooter.right.text = "Página &P de &N"

    # GUARDAR EN MEMORIA

    archivo = BytesIO()

    libro.save(archivo)

    archivo.seek(0)

    return archivo


# ==========================================
# COLUMNAS DEL REPORTE DE POSTULACIONES
# ==========================================

COLUMNAS_POSTULACIONES = [
    {"titulo": "Estudiante", "campo": "__estudiante__", "peso": 1.3, "ancho": 28},
    {"titulo": "Código estudiantil", "campo": "codigo_estudiantil", "peso": 1, "ancho": 22},
    {"titulo": "Programa académico", "campo": "programa_academico", "peso": 1.4, "ancho": 32},
    {"titulo": "Puesto de práctica", "campo": "puesto_practica", "peso": 1.3, "ancho": 30},
    {"titulo": "Empresa", "campo": "empresa", "peso": 1.2, "ancho": 28},
    {"titulo": "Estado", "campo": "estado", "peso": 0.8, "ancho": 18},
    {"titulo": "Fecha de postulación", "campo": "fecha_postulacion", "peso": 1, "ancho": 24}
]


# ==========================================
# COLUMNAS DEL REPORTE DE PRÁCTICAS
# ==========================================

COLUMNAS_PRACTICAS = [
    {"titulo": "Estudiante", "campo": "__estudiante__", "peso": 1.3, "ancho": 28},
    {"titulo": "Código estudiantil", "campo": "codigo_estudiantil", "peso": 1, "ancho": 22},
    {"titulo": "Programa académico", "campo": "programa_academico", "peso": 1.3, "ancho": 30},
    {"titulo": "Empresa", "campo": "empresa", "peso": 1.2, "ancho": 28},
    {"titulo": "Puesto de práctica", "campo": "puesto_practica", "peso": 1.2, "ancho": 28},
    {"titulo": "Tutor", "campo": "__tutor__", "peso": 1.2, "ancho": 26},
    {"titulo": "Fecha de inicio", "campo": "fecha_inicio", "peso": 0.9, "ancho": 18},
    {"titulo": "Fecha de finalización", "campo": "fecha_fin", "peso": 1, "ancho": 20},
    {"titulo": "Horas requeridas", "campo": "horas_requeridas", "peso": 0.8, "ancho": 18},
    {"titulo": "Horas completadas", "campo": "horas_completadas", "peso": 0.8, "ancho": 18},
    {"titulo": "Objetivo", "campo": "objetivo", "peso": 1.8, "ancho": 40},
    {"titulo": "Estado", "campo": "estado", "peso": 0.8, "ancho": 18}
]


# ==========================================
# COLUMNAS DEL REPORTE DE EVALUACIONES
# ==========================================

COLUMNAS_EVALUACIONES = [
    {"titulo": "Estudiante", "campo": "__estudiante__", "peso": 1.2, "ancho": 28},
    {"titulo": "Código estudiantil", "campo": "codigo_estudiantil", "peso": 0.9, "ancho": 22},
    {"titulo": "Programa académico", "campo": "programa_academico", "peso": 1.1, "ancho": 30},
    {"titulo": "Empresa", "campo": "empresa", "peso": 1, "ancho": 26},
    {"titulo": "Puesto de práctica", "campo": "puesto_practica", "peso": 1, "ancho": 26},
    {"titulo": "Tutor", "campo": "__tutor__", "peso": 1, "ancho": 25},
    {"titulo": "Evaluador", "campo": "__evaluador__", "peso": 1, "ancho": 25},
    {"titulo": "Tipo de evaluación", "campo": "tipo_evaluacion", "peso": 0.9, "ancho": 22},
    {"titulo": "Fecha de evaluación", "campo": "fecha_evaluacion", "peso": 0.9, "ancho": 22},
    {"titulo": "Resultado", "campo": "resultado", "peso": 0.8, "ancho": 18},
    {"titulo": "Calificación", "campo": "calificacion", "peso": 0.7, "ancho": 16},
    {"titulo": "Cumplimiento de objetivos", "campo": "cumplimiento_objetivos", "peso": 1.4, "ancho": 35},
    {"titulo": "Desempeño", "campo": "desempeno", "peso": 1.3, "ancho": 32},
    {"titulo": "Fortalezas", "campo": "fortalezas", "peso": 1.2, "ancho": 30},
    {"titulo": "Aspectos de mejora", "campo": "aspectos_mejora", "peso": 1.2, "ancho": 30},
    {"titulo": "Observaciones", "campo": "observaciones", "peso": 1.3, "ancho": 35},
    {"titulo": "Recomendaciones", "campo": "recomendaciones", "peso": 1.3, "ancho": 35},
    {"titulo": "Estado", "campo": "estado", "peso": 0.8, "ancho": 18}
]


# ==========================================
# FUNCIONES PÚBLICAS: POSTULACIONES
# ==========================================

def generar_pdf_postulaciones(datos):

    return generar_pdf_general(
        datos,
        "REPORTE DE POSTULACIONES",
        COLUMNAS_POSTULACIONES
    )


def generar_excel_postulaciones(datos):

    return generar_excel_general(
        datos,
        "Postulaciones",
        "REPORTE DE POSTULACIONES",
        COLUMNAS_POSTULACIONES
    )


# ==========================================
# FUNCIONES PÚBLICAS: PRÁCTICAS
# ==========================================

def generar_pdf_practicas(datos):

    return generar_pdf_general(
        datos,
        "REPORTE DE PRÁCTICAS",
        COLUMNAS_PRACTICAS
    )


def generar_excel_practicas(datos):

    return generar_excel_general(
        datos,
        "Practicas",
        "REPORTE DE PRÁCTICAS",
        COLUMNAS_PRACTICAS
    )


# ==========================================
# FUNCIONES PÚBLICAS: EVALUACIONES
# ==========================================

def generar_pdf_evaluaciones(datos):

    return generar_pdf_general(
        datos,
        "REPORTE DE EVALUACIONES",
        COLUMNAS_EVALUACIONES
    )


def generar_excel_evaluaciones(datos):

    return generar_excel_general(
        datos,
        "Evaluaciones",
        "REPORTE DE EVALUACIONES",
        COLUMNAS_EVALUACIONES
    )
