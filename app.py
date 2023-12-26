from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, make_response
import pdfkit


app = Flask(__name__)

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

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():

    # Ruta al ejecutable wkhtmltopdf en tu sistema
    ruta_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
    
    try:
        datos_recibidos = request.json.get('datos')
        print(datos_recibidos)

        # Construir el contenido del PDF usando los datos recibidos
        contenido_pdf = '<h1>Información del LocalStorage</h1>'
        contenido_pdf += '<ul>'
        for data in datos_recibidos:
            contenido_pdf += f'<li>{data}</li>'
        contenido_pdf += '</ul>'

        pdfkit_options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',  # Especificar la codificación UTF-8
            # Otras opciones de configuración si las necesitas
        }

        # Generar el PDF
        pdf = pdfkit.from_string(contenido_pdf, False, configuration=config, options=pdfkit_options)

        # Crear la respuesta con el PDF como descarga
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=mi_pdf.pdf'

        return response
    except Exception as e:
        print("Error:", e)  # Imprime el error en la consola del servidor
        return "Error al generar el PDF", 500


if __name__ == '__main__':
    app.run(debug=True)