import pdfkit
from flask import render_template, request, url_for, session, abort, flash


def generar_factura(estudio):

    path_wkthmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    html = render_template("pdfs/presupuesto.html", estudio="asdasdas")
    # html = render_template("pdfs/presupuesto.html", estudio=estudio)

    ruta_archivo = "archivos/facturas/factura_" + "555" + ".pdf"
    # ruta_archivo = "archivos/facturas/factura_" + estudio.id + ".pdf"

    pdfkit.from_string(html, ruta_archivo, configuration=config)
