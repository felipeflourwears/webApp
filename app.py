from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, make_response
import pdfkit


app = Flask(__name__)

# Establecer la ruta a wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_string('Hello World!', 'out.pdf', configuration=config)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pdf', methods=['POST'])
def generar_pdf_desde_datos():
    datos_recibidos = request.json.get('datos')

    if datos_recibidos:  
        for batch in datos_recibidos:
            print(batch)
        
        # Puedes realizar el procesamiento para generar el PDF aquí
        
        return 'Datos de todos los lotes recibidos. Procesamiento del PDF en curso...LF'
    else:
        return 'Datos vacíos recibidos. No se puede procesar.'

@app.route('/generar_pdf', methods=['GET'])
def generar_pdf():
    pdfkit_options = {
        'page-size': 'A4',
        # Otras opciones de configuración si las necesitas
    }

    # Contenido del PDF que quieres generar
    contenido_pdf = '<h1>¡Hola, este es tu PDF generado con Flask y pdfkit!</h1>'

    pdf = pdfkit.from_string(contenido_pdf, False, configuration=config, options=pdfkit_options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=mi_pdf.pdf'

    return response


if __name__ == '__main__':
    app.run(debug=True)