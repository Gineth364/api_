
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
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
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table as ExcelTable
from openpyxl.worksheet.table import TableStyleInfo


def generar_pdf_postulaciones(datos):

    archivo = BytesIO()

    documento = SimpleDocTemplate(
        archivo,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=35,
        bottomMargin=35
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
        textColor=colors.white,
        alignment=TA_CENTER
    )

    contenido = ParagraphStyle(
        "ContenidoTabla",
        parent=estilos["Normal"],
        fontSize=7,
        leading=9,
        alignment=TA_LEFT
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

    elementos.append(Spacer(1, 8))

    elementos.append(
        Paragraph(
            "<b>REPORTE DE POSTULACIONES</b>",
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
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Total de registros: {len(datos)}",
            estilos["Normal"]
        )
    )

    elementos.append(Spacer(1, 15))

    columnas = [
        "Estudiante",
        "Código",
        "Programa académico",
        "Puesto de práctica",
        "Empresa",
        "Estado",
        "Fecha"
    ]

    tabla_datos = [
        [Paragraph(columna, encabezado) for columna in columnas]
    ]

    for fila in datos:
        estudiante = (
            f"{fila['nombre_estudiante']} "
            f"{fila['apellido_estudiante']}"
        )

        tabla_datos.append([
            Paragraph(estudiante, contenido),
            Paragraph(str(fila["codigo_estudiantil"]), contenido),
            Paragraph(str(fila["programa_academico"]), contenido),
            Paragraph(str(fila["puesto_practica"]), contenido),
            Paragraph(str(fila["empresa"]), contenido),
            Paragraph(str(fila["estado"]), contenido),
            Paragraph(
                fila["fecha_postulacion"].strftime("%d/%m/%Y %H:%M")
                if isinstance(fila["fecha_postulacion"], datetime)
                else str(fila["fecha_postulacion"]),
                contenido
            )
        ])

    tabla = Table(
        tabla_datos,
        colWidths=[90, 65, 110, 110, 105, 80, 90],
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173B67")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DFEA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
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
            30,
            20,
            "UniPrácticas | Reporte de postulaciones"
        )

        canvas.drawRightString(
            documento.pagesize[0] - 30,
            20,
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


def generar_excel_postulaciones(datos):

    libro = Workbook()
    hoja = libro.active

    hoja.title = "Postulaciones"

    azul = "173B67"
    azul_claro = "DCEAF7"
    blanco = "FFFFFF"

    hoja.merge_cells("A1:G1")
    hoja["A1"] = "UniPrácticas"

    hoja["A1"].font = Font(
        name="Arial",
        size=18,
        bold=True,
        color=blanco
    )

    hoja["A1"].fill = PatternFill(
        fill_type="solid",
        fgColor=azul
    )

    hoja["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    hoja.row_dimensions[1].height = 32

    hoja.merge_cells("A2:G2")
    hoja["A2"] = (
        "Sistema de Seguimiento de Prácticas Profesionales"
    )

    hoja["A2"].font = Font(
        name="Arial",
        size=10,
        italic=True,
        color=azul
    )

    hoja["A2"].alignment = Alignment(horizontal="center")

    hoja.merge_cells("A4:G4")
    hoja["A4"] = "REPORTE DE POSTULACIONES"

    hoja["A4"].font = Font(
        size=14,
        bold=True,
        color=azul
    )

    hoja["A4"].alignment = Alignment(horizontal="center")

    hoja["A5"] = "Fecha de generación:"
    hoja["B5"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    hoja["A6"] = "Total de registros:"
    hoja["B6"] = len(datos)

    encabezados = [
        "Estudiante",
        "Código estudiantil",
        "Programa académico",
        "Puesto de práctica",
        "Empresa",
        "Estado",
        "Fecha de postulación"
    ]

    fila_encabezado = 8

    for columna, nombre in enumerate(encabezados, start=1):
        celda = hoja.cell(
            row=fila_encabezado,
            column=columna,
            value=nombre
        )

        celda.font = Font(bold=True, color=blanco)
        celda.fill = PatternFill(
            fill_type="solid",
            fgColor=azul
        )

        celda.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    for numero_fila, fila in enumerate(datos, start=9):

        estudiante = (
            f"{fila['nombre_estudiante']} "
            f"{fila['apellido_estudiante']}"
        )

        valores = [
            estudiante,
            fila["codigo_estudiantil"],
            fila["programa_academico"],
            fila["puesto_practica"],
            fila["empresa"],
            fila["estado"],
            fila["fecha_postulacion"]
        ]

        for columna, valor in enumerate(valores, start=1):
            celda = hoja.cell(
                row=numero_fila,
                column=columna,
                value=valor
            )

            celda.fill = PatternFill(
                fill_type="solid",
                fgColor=blanco if numero_fila % 2 else azul_claro
            )

            celda.alignment = Alignment(
                vertical="center",
                wrap_text=True
            )

            celda.border = Border(
                bottom=Side(
                    style="thin",
                    color="D5DFEA"
                )
            )

            if columna == 7 and isinstance(valor, datetime):
                celda.number_format = "dd/mm/yyyy hh:mm"

    anchos = [28, 22, 32, 32, 30, 20, 25]

    for columna, ancho in enumerate(anchos, start=1):
        hoja.column_dimensions[
            get_column_letter(columna)
        ].width = ancho

    hoja.freeze_panes = "A9"
    hoja.auto_filter.ref = f"A8:G{max(8, len(datos) + 8)}"

    hoja.sheet_view.showGridLines = False

    hoja.oddFooter.center.text = "UniPrácticas | Reporte de postulaciones"
    hoja.oddFooter.right.text = "Página &P de &N"

    archivo = BytesIO()
    libro.save(archivo)
    archivo.seek(0)

    return archivo
