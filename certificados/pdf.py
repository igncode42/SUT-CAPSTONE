from io import BytesIO
from xml.sax.saxutils import escape

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


COLOR_PRIMARIO = colors.HexColor("#2F624A")
COLOR_TEXTO = colors.HexColor("#202923")
COLOR_SECUNDARIO = colors.HexColor("#627067")
COLOR_BORDE = colors.HexColor("#D9E1DA")
COLOR_SUAVE = colors.HexColor("#EDF4EE")
COLOR_FONDO = colors.HexColor("#F6F4EF")


MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def _numero_certificado(certificado):
    return f"SUT-CR-{certificado.pk:06d}"


def _formatear_fecha(fecha):
    fecha_local = timezone.localtime(fecha)

    return (
        f"{fecha_local.day} de "
        f"{MESES[fecha_local.month]} de "
        f"{fecha_local.year}"
    )


def nombre_archivo_certificado(certificado):
    return (
        "certificado-residencia-"
        f"{_numero_certificado(certificado)}.pdf"
    )


def _dibujar_pagina(canvas, doc):
    ancho, alto = A4

    canvas.saveState()

    # Línea institucional superior
    canvas.setStrokeColor(COLOR_PRIMARIO)
    canvas.setLineWidth(1.4)
    canvas.line(
        20 * mm,
        alto - 18 * mm,
        ancho - 20 * mm,
        alto - 18 * mm,
    )

    # Pie de página
    canvas.setStrokeColor(COLOR_BORDE)
    canvas.setLineWidth(0.5)
    canvas.line(
        20 * mm,
        17 * mm,
        ancho - 20 * mm,
        17 * mm,
    )

    canvas.setFillColor(COLOR_SECUNDARIO)
    canvas.setFont(
        "Helvetica",
        7.5,
    )

    canvas.drawString(
        20 * mm,
        11 * mm,
        "Sistema Unidad Territorial · Documento generado electrónicamente",
    )

    canvas.drawRightString(
        ancho - 20 * mm,
        11 * mm,
        f"Página {doc.page}",
    )

    canvas.restoreState()


def generar_certificado_pdf(certificado):
    """
    Genera el certificado de residencia en memoria.

    Retorna:
        bytes: contenido completo del archivo PDF.
    """

    if certificado.pk is None:
        raise ValueError(
            "El certificado debe estar guardado antes de generar el PDF."
        )

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=24 * mm,
        leftMargin=24 * mm,
        topMargin=28 * mm,
        bottomMargin=25 * mm,
        title="Certificado de residencia",
        author="Sistema Unidad Territorial",
        subject="Certificado de residencia emitido por el SUT",
    )


    # ========================================================
    # ESTILOS
    # ========================================================

    estilos_base = getSampleStyleSheet()

    estilo_marca = ParagraphStyle(
        "MarcaSUT",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=COLOR_PRIMARIO,
        alignment=TA_CENTER,
        spaceAfter=3 * mm,
    )

    estilo_institucion = ParagraphStyle(
        "InstitucionSUT",
        parent=estilos_base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=COLOR_SECUNDARIO,
        alignment=TA_CENTER,
        spaceAfter=10 * mm,
    )

    estilo_titulo = ParagraphStyle(
        "TituloCertificado",
        parent=estilos_base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        textColor=COLOR_TEXTO,
        alignment=TA_CENTER,
        spaceAfter=3 * mm,
    )

    estilo_numero = ParagraphStyle(
        "NumeroCertificado",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=COLOR_PRIMARIO,
        alignment=TA_CENTER,
        spaceAfter=10 * mm,
    )

    estilo_cuerpo = ParagraphStyle(
        "CuerpoCertificado",
        parent=estilos_base["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=18,
        textColor=COLOR_TEXTO,
        alignment=TA_LEFT,
        spaceAfter=6 * mm,
    )

    estilo_cuerpo_centrado = ParagraphStyle(
        "CuerpoCentrado",
        parent=estilo_cuerpo,
        alignment=TA_CENTER,
    )

    estilo_etiqueta = ParagraphStyle(
        "EtiquetaDato",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=COLOR_SECUNDARIO,
    )

    estilo_valor = ParagraphStyle(
        "ValorDato",
        parent=estilos_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=COLOR_TEXTO,
    )

    estilo_nota = ParagraphStyle(
        "NotaCertificado",
        parent=estilos_base["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=13,
        textColor=COLOR_SECUNDARIO,
        alignment=TA_CENTER,
    )


    # ========================================================
    # DATOS
    # ========================================================

    nombre_completo = (
        f"{certificado.nombre_vecino} "
        f"{certificado.apellido_vecino}"
    ).strip()

    nombre_seguro = escape(nombre_completo)

    identificacion_segura = escape(
        certificado.identificacion_vecino
    )

    direccion_segura = escape(
        certificado.direccion_vecino
    )

    numero = _numero_certificado(
        certificado
    )

    fecha_emision = _formatear_fecha(
        certificado.fecha_emision
    )


    # ========================================================
    # CONTENIDO
    # ========================================================

    contenido = []


    contenido.append(
        Paragraph(
            "SUT",
            estilo_marca,
        )
    )

    contenido.append(
        Paragraph(
            "Sistema Unidad Territorial",
            estilo_institucion,
        )
    )


    contenido.append(
        Paragraph(
            "CERTIFICADO DE RESIDENCIA",
            estilo_titulo,
        )
    )

    contenido.append(
        Paragraph(
            f"Documento N.º {numero}",
            estilo_numero,
        )
    )


    contenido.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=COLOR_PRIMARIO,
            spaceBefore=0,
            spaceAfter=10 * mm,
        )
    )


    contenido.append(
        Paragraph(
            (
                "El <b>Sistema Unidad Territorial (SUT)</b> "
                "certifica que:"
            ),
            estilo_cuerpo_centrado,
        )
    )


    contenido.append(
        Spacer(
            1,
            3 * mm,
        )
    )


    datos = [
        [
            Paragraph(
                "NOMBRE COMPLETO",
                estilo_etiqueta,
            ),
            Paragraph(
                nombre_seguro,
                estilo_valor,
            ),
        ],
        [
            Paragraph(
                "IDENTIFICACIÓN",
                estilo_etiqueta,
            ),
            Paragraph(
                identificacion_segura,
                estilo_valor,
            ),
        ],
        [
            Paragraph(
                "DOMICILIO REGISTRADO",
                estilo_etiqueta,
            ),
            Paragraph(
                direccion_segura,
                estilo_valor,
            ),
        ],
    ]


    tabla_datos = Table(
        datos,
        colWidths=[
            48 * mm,
            102 * mm,
        ],
        hAlign="CENTER",
    )

    tabla_datos.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    COLOR_SUAVE,
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, -1),
                    colors.white,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    COLOR_BORDE,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    COLOR_BORDE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )


    contenido.append(
        tabla_datos
    )

    contenido.append(
        Spacer(
            1,
            10 * mm,
        )
    )


    contenido.append(
        Paragraph(
            (
                f"La persona individualizada registra domicilio en "
                f"<b>{direccion_segura}</b>, de acuerdo con la "
                "información registrada en el Sistema Unidad Territorial "
                "al momento de la emisión del presente documento."
            ),
            estilo_cuerpo,
        )
    )


    contenido.append(
        Paragraph(
            (
                "El presente certificado se emite a solicitud del "
                "interesado para los fines que estime pertinentes."
            ),
            estilo_cuerpo,
        )
    )


    contenido.append(
        Spacer(
            1,
            7 * mm,
        )
    )


    emision = [
        [
            Paragraph(
                "FECHA DE EMISIÓN",
                estilo_etiqueta,
            ),
            Paragraph(
                fecha_emision,
                estilo_valor,
            ),
        ],
        [
            Paragraph(
                "SOLICITUD",
                estilo_etiqueta,
            ),
            Paragraph(
                f"#{certificado.solicitud_id}",
                estilo_valor,
            ),
        ],
        [
            Paragraph(
                "ESTADO",
                estilo_etiqueta,
            ),
            Paragraph(
                "Emitido",
                estilo_valor,
            ),
        ],
    ]


    tabla_emision = Table(
        emision,
        colWidths=[
            48 * mm,
            102 * mm,
        ],
        hAlign="CENTER",
    )

    tabla_emision.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    COLOR_FONDO,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    COLOR_BORDE,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    COLOR_BORDE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )


    contenido.append(
        tabla_emision
    )

    contenido.append(
        Spacer(
            1,
            12 * mm,
        )
    )


    contenido.append(
        Paragraph(
            (
                "Documento generado electrónicamente por el "
                "<b>Sistema Unidad Territorial</b>. "
                "Los datos corresponden al registro existente "
                "al momento de su emisión."
            ),
            estilo_nota,
        )
    )


    # ========================================================
    # GENERAR
    # ========================================================

    documento.build(
        contenido,
        onFirstPage=_dibujar_pagina,
        onLaterPages=_dibujar_pagina,
    )

    pdf = buffer.getvalue()

    buffer.close()

    return pdf