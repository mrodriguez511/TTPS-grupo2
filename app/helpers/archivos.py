import pdfkit
import os,sys, subprocess, platform
from flask import render_template, current_app, request, url_for, session, abort, flash
from app.models.tipoEstudio import TipoEstudio
from app.models.paciente import Paciente
from app.models.estudio import Estudio


def generar_factura(estudio):

    #path_wkthmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    #config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    tipoEstudio = TipoEstudio.query.filter(
        TipoEstudio.id == estudio.tipoEstudio
    ).first()
    paciente = Paciente.query.filter(Paciente.id == estudio.paciente).first()
    html = render_template(
        "pdfs/presupuesto.html", estudio=estudio, tipo=tipoEstudio, receptor=paciente
    )
    ruta = current_app.config["UPLOADED_FACTURAS_DEST"]
    nombre_archivo = "presupuesto_" + str(estudio.id) + ".pdf"
    ruta_archivo = os.path.join(ruta, nombre_archivo)
    
    if 'DYNO' in os.environ:
        print ('loading wkhtmltopdf path on heroku')
        config = subprocess.Popen(
            ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')], # Note we default to 'wkhtmltopdf' as the binary name
            stdout=subprocess.PIPE).communicate()[0].strip()
    
    
    pdfkit.from_string(html, ruta_archivo, configuration=config)

    return nombre_archivo


# https://stackoverflow.com/questions/52721272/python-3-flask-install-wkhtmltopdf-on-heroku


"""
https://stackoverflow.com/questions/54707110/how-to-get-wkhtmltopdf-working-on-heroku
def _get_pdfkit_config():
     wkhtmltopdf lives and functions differently depending on Windows or Linux. We
      need to support both since we develop on windows but deploy on Heroku.

     Returns:
         A pdfkit configuration
     
     if platform.system() == 'Windows':
         return pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
     else:
         WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
         return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
         
         
         
         
         if platform.system() == "Windows":
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
else:
        os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable) 
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], 
            stdout=subprocess.PIPE).communicate()[0].strip()
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
        
        
        
        https://github-releases.githubusercontent.com/271714/70314134-52da-11e7-81d9-a3f151bef518?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20211027%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211027T210800Z&X-Amz-Expires=300&X-Amz-Signature=8aafc23ab4bcb8a903decd3c079cf04dd779b6be6e6318495afcdd005ffd581d&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=271714&response-content-disposition=attachment%3B%20filename%3Dwkhtmltox-0.12.4_msvc2015-win64.exe&response-content-type=application%2Foctet-stream"""
