from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, make_response
import pdfkit
import os
import base64
from collections import defaultdict


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def calcular_descuento_por_lotes(cantidad_lotes):
    if 150 <= cantidad_lotes <= 500:
        return 0.00  # Sin descuento
    elif 501 <= cantidad_lotes <= 1000:
        return 0.02  # Descuento del 2%
    elif 1001 <= cantidad_lotes <= 2000:
        return 0.035  # Descuento del 3.5%
    elif 2001 <= cantidad_lotes <= 3000:
        return 0.05  # Descuento del 5%
    elif cantidad_lotes > 3000:
        return 0.075  # Descuento del 7.5%
    else:
        return 0 

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
    #Data Frontend
    datos_recibidos = request.json.get('datos')

    

    # Ruta al ejecutable wkhtmltopdf en tu sistema
    ruta_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
    
    # Ruta del directorio actual del script
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    # Ruta de la imagen
    ruta_imagen = os.path.join(ruta_script, 'static','images', 'black.jpg')
    print("RUTA Imagen: ", ruta_imagen)

    # Leer la imagen en formato base64
    with open(ruta_imagen, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    #Obligatory Requirements
   
    video_procesor = 377.988
    freight_import_taxes = 487.20
    install = 931.02
    cms = 152.1
    noc = 720
    totalFixed = 0

    #Calcular la suma de los precios
    totalFixed = video_procesor + freight_import_taxes + install + cms + noc

    # Define the dictionary with a default value of 0 for new keys
    precios_por_tamano = defaultdict(float, {
        'Pitch 2 120 Header': 1392.391,
        'Pitch 1.8 120 Header': 2086.5,
        'Pitch 1.5 120 Header': 2386.8,
        'Pitch 1.2 120 Header': 3110.276,

        'Pitch 2 90 Header': 1189.864,
        'Pitch 1.8 90 Header': 1431.3,
        'Pitch 1.5 90 Header': 1627.47,
        'Pitch 1.2 90 Header': 2386.956,

        'Pitch 2 60 Header': 848.9,
        'Pitch 1.8 60 Header': 1171.3,
        'Pitch 1.5 60 Header': 1232.4,
        'Pitch 1.2 60 Header': 1656.2,

        'Pitch 2 45 Header': 848.9,
        'Pitch 1.8 45 Header': 1171.3,
        'Pitch 1.5 45 Header': 1232.4,
        'Pitch 1.2 45 Header': 1656.2,

        'Pitch 1.8 120 Shelf': 640.9,
        'Pitch 1.5 120 Shelf': 672.1,
        'Pitch 1.2 120 Shelf': 861.9,

        'Pitch 1.8 90 Shelf': 456.3,
        'Pitch 1.5 90 Shelf': 533,
        'Pitch 1.2 90 Shelf': 655.2,

        'Pitch 1.8 60 Shelf': 362.7,
        'Pitch 1.5 60 Shelf': 440.7,
        'Pitch 1.2 60 Shelf': 487.5,

        'Pitch 1.8 45 Shelf': 555.1,
        'Pitch 1.5 45 Shelf': 617.5,
        'Pitch 1.2 45 Shelf': 679.9
    })
    
    #Total Mandatory Items
    # Obtener la suma de las cantidades de los elementos de tipo "Mandatory items"
    quantityMandatoryItems = sum(int(data['quantity']) for data in datos_recibidos if data['type'] == 'Mandatory items')

    # Multiplicar la suma por totalFixed
    totalMandatoryItems = '{:,.3f}'.format(quantityMandatoryItems * totalFixed)

    print("quantityMandatoryItems: ", quantityMandatoryItems)
    print("totalMandatoryItems: ", totalMandatoryItems)
    
    
    
    try:
        print("DATA PDF: ", datos_recibidos)

        # Procesamiento para calcular totales de Header y Shelf por lote
        totales_lote = []
        grand_total_lote = []
        total_por_tipo = defaultdict(float)
        contador = 0
        informacion_lotes = []

        for lote in datos_recibidos:
            tipo = lote['type']
            tamano = lote['size']
            cantidad = int(lote['quantity'])

            precio_por_item = precios_por_tamano.get(tamano, 0)
            precio_total_por_item = precio_por_item * cantidad
            print("COL: ", cantidad, tipo, tamano, precio_por_item, precio_total_por_item)

            if tipo in ('Header', 'Shelf'):
                total_por_tipo[tipo] += precio_total_por_item
                
            elif tipo == 'Mandatory items':
                totales_lote.append(total_por_tipo.copy())
                grand_total_lote.append(total_por_tipo.copy())
                total_por_tipo = defaultdict(float)

                # Calcular los totales de Header y Shelf para el lote actual
                totales_headers = sum(l['Header'] for l in totales_lote)
                totales_shelfs = sum(l['Shelf'] for l in totales_lote)
                total_option = totales_headers + totales_shelfs
                print(lote, " HEADER T: ", totales_headers)
                print(lote, " SHELFS T: ", totales_shelfs)
                print(lote, " TotalOption T: ", total_option)

                # Reiniciar los totales a cero para el próximo lote
                totales_lote = []
                totales_headers = 0
                totales_shelfs = 0

        totales_headers_g = sum(l['Header'] for l in grand_total_lote)
        totales_shelfs_g = sum(l['Shelf'] for l in grand_total_lote)
        total_smart_display = totales_shelfs_g + totales_headers_g
        print("H: ", totales_headers_g)
        print("S: ", totales_shelfs_g)
        print("Total Smart Display: ", total_smart_display)

        contenido_pdf = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Smart Budget PopAtelier</title>
                <style>
                    header {{
                        text-align: center;
                    }}
                    img {{
                        max-width: 500px;
                    }}
                    .info {{
                        text-align: left;
                        font-size: 20px;
                        margin-top: 10px;
                        margin-left: 10px;
                    }}
                    .table-container {{
                        margin-top: 20px;
                        margin-left: 10px;
                        width: 98%;
                    }}
                    .headers-doc{{
                        margin-top: 50px;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin-top: 10px;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                        vertical-align: top; /* Alineación vertical */
                        line-height: 1.4; /* Ajuste del espaciado vertical */
                    }}
                    th {{
                        background-color: black;
                        color: white;
                        text-align: center;
                    }}
                    hr {{
                        margin-top: 50px;
                        border: none;
                        border-top: 2px solid black;
                        width: 100%;
                    }}
                    .total-left{{
                        text-align: right;
                    }}
                    .grand-total {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 10px;
                    }}

                    .grand-total table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}

                    .grand-total th,
                    .grand-total td {{
                        border: 1px solid black;
                        padding: 8px;
                        text-align: right;
                    }}

                    .grand-total th:nth-child(1),
                    .grand-total td:nth-child(1) {{
                        width: 200px; /* Ancho fijo para el primer columna (Total mandatory items y Total smart display kits) */
                    }}

                    .grand-total th:nth-child(2),
                    .grand-total td:nth-child(2) {{
                        width: 150px; /* Ancho fijo para el segunda columna ($ 1,404.0) */
                    }}

                    .grand-total th:nth-child(3),
                    .grand-total td:nth-child(3) {{
                        width: 150px; /* Ancho fijo para el tercera columna (Grand Total y $ 4,072.31) */
                    }}

                    .grand-total th {{
                        background-color: black;
                        color: white;
                        text-align: left;
                    }}
                    .feauture-total {{
                        font-size: 20px;
                    }}
                </style>
            </head>
            <body>
                <header>
                    <img src="data:image/jpeg;base64,{img_base64}" alt="Logo"> <!-- Imagen incrustada en formato base64 -->
                    <div class="info">
                        <p><strong>POP ATELIER LLC</strong></p>
                        <p><strong>Concept:</strong> Quotation</p>
                        <p><strong>Date:</strong> 5/12/2023</p>
                    </div>
                </header>
                <div class="table-container">
                    <h2 class="headers-doc">Mandatory items: </h2>
                    <table>
                        <tr>
                            <th>Item</th>
                            <th>Cost</th>
                        </tr>
                        <tr>
                            <td>Video processor + 4G card</td>
                            <td class="total-left">$ 377.99</td>
                        </tr>
                        <tr>
                            <td>Freight + import taxes</td>
                            <td class="total-left">$ 487.20</td>
                        </tr>
                        <tr>
                            <td>Installation</td>
                            <td class="total-left">$ 931.02</td>
                        </tr>
                        <tr>
                            <td>CMS annual fee</td>
                            <td class="total-left">$ 152.10</td>
                        </tr>
                        <tr>
                            <td>NOC + cell data annual fee</td>
                            <td class="total-left">$ 152.10</td>
                        </tr>
                        <tr>
                            <td><strong>Total</strong></td>
                            <td class="total-left"><strong>$ 2,668.31</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Mandatory items: {quantityMandatoryItems}</strong></td>
                            <td class="total-left"><strong>$ {totalMandatoryItems}</strong></td>
                        </tr>
                    </table>
                </div>
        """

        # Construir el contenido del PDF usando los datos recibidos
        contenido_pdf += """
            <hr>
            <h2 class="headers-doc">Smart Display Kit: </h2>
            <hr>
            <div class="table-container">
        """

        for lote in datos_recibidos:
            
            tipo = lote['type']
            tamano = lote['size']
            cantidad = int(lote['quantity'])

            
            # Crear un diccionario con la información del lote actual y agregarlo al arreglo
            if(tipo!="Mandatory items"):
                precio_por_item = precios_por_tamano.get(tamano, 0)
                precio_total_por_item = precio_por_item * cantidad
                informacion_lote_actual = {
                    'tipo': tipo,
                    'tamano': tamano,
                    'cantidad': cantidad,
                    'precio_por_item': precio_por_item,
                    'precio_total_por_item': precio_total_por_item
                        # Puedes agregar más información si es necesaria
                }
    
                informacion_lotes.append(informacion_lote_actual)
            else:
                totalM = totalFixed * cantidad
                totalMF = "${:,.3f}".format(totalM)
                informacion_lote_actual = {
                    'tipo': tipo,
                    'tamano': "---",
                    'cantidad': cantidad,
                    'precio_por_item': totalFixed,
                    'precio_total_por_item': totalMF
                        # Puedes agregar más información si es necesaria
                }
                informacion_lotes.append(informacion_lote_actual)

            if tipo in ('Header', 'Shelf'):
                total_por_tipo[tipo] += precio_total_por_item
                totales_lote.append(total_por_tipo.copy())
                total_por_tipo = defaultdict(float)
                # Reiniciar los totales a cero para el próximo lote
                totales_lote = []
                totales_headers = 0
                totales_shelfs = 0
                
        print("INFORMACION de lotes ", informacion_lotes)

        cont = 0
        option = 0
        headerst = 0
        shelfst = 0
        grand_total_hsm = 0
        gran_total_smart_display = 0
        for lot in informacion_lotes:
            tipoL = lot['tipo']
            tamanoL = lot['tamano']
            cantidadL = lot['cantidad']
            precio_por_itemL = lot['precio_por_item']
            precio_total_por_itemL = lot['precio_total_por_item']

            if cont == 0:
                option += 1
                contenido_pdf += f"""
                <h3 class="">Option {option}: </h3>
                <table>
                <tr>
                    <th>Quantity</th>
                    <th>Type</th>
                    <th>Size</th>
                    <th>Price per item</th>
                    <th>Total price per item</th>
                </tr> """
            if tipoL in ('Header', 'Shelf'):
                if(tipoL == "Header"):
                    headerst += precio_total_por_itemL
                else:
                    shelfst += precio_total_por_itemL
                contenido_pdf += f"""
                <tr>
                    <td>{cantidadL}</td>
                    <td>{tipoL}</td>
                    <td>{tamanoL}</td>
                    <td>{precio_por_itemL}</td>
                    <td class="total-left">{precio_total_por_itemL}</td>
                </tr> """
                cont = 1
            elif tipoL == "Mandatory items":
                headerst *= cantidadL
                shelfst *= cantidadL
                # Realizar el cálculo del 'grand_total_hsm'
                gran_total_smart_display += headerst
                gran_total_smart_display += shelfst
                grand_total_hsm = headerst + shelfst + cantidadL * totalFixed

                # Formatear con comas como separadores de miles
                grand_total_hsm_formatted = "{:,.3f}".format(grand_total_hsm)
                shelfst_formatted = "{:,.3f}".format(shelfst)
                headerst_formatted = "{:,.3f}".format(headerst)


                contenido_pdf += f"""
                <tr>
                    <td>{cantidadL}</td>
                    <td>{tipoL}</td>
                    <td>{tamanoL}</td>
                    <td>{precio_por_itemL}</td>
                    <td class="total-left"><strong>{precio_total_por_itemL}</strong></td>
                </tr> 
                """

                #contenido_pdf
                """
                <tr>
                    <td><strong>Smart Display</strong></td>
                    <td class="total-left" colspan="4"><strong>{cantidadL}</strong></td>
                </tr>
                """
                contenido_pdf += f"""
                <tr>
                    <td><strong>Headers Total</strong></td>
                    <td class="total-left" colspan="4"><strong>$ {headerst_formatted}</strong></td>
                </tr>
                <tr>
                    <td><strong>Shelfs Total</strong></td>
                    <td class="total-left" colspan="4"><strong>$ {shelfst_formatted}</strong></td>
                </tr>
                <tr>
                    <td><strong>Total Option {option}</strong></td>
                    <td class="total-left" colspan="4"><strong>$ {grand_total_hsm_formatted}</strong></td>
                </tr>
                """
                headerst = 0
                shelfst = 0
                grand_total_hsm = 0
                cont = 0  # Establecer cont a 1, asumo que esa es tu intención
                contenido_pdf += f"""</table> """

        ##Totales Formatted
        gran_total_smart_display_formatted = "{:,.3f}".format(gran_total_smart_display)

        contenido_pdf += f"""
        <hr>
        <br>
            <div class="grand-total">
                <table>
                    <tr>
                        <th class="feauture-total">Total mandatory items:</th>
                        <td class="feauture-total"><strong>$ {totalMandatoryItems}</strong></td>
                    </tr>
                </table>
            </div>
            <div class="grand-total">
                <table>
                    <tr>
                        <th class="feauture-total">Total smart display kits:</th>
                        <td class="feauture-total"><strong>$ {gran_total_smart_display_formatted}</strong></td>
                    </tr>
                </table>
            </div>
            """
        grand_total = 0
        totalMandatoryItems = totalMandatoryItems.replace(',', '')
        # Convertir el número limpio a un tipo de dato float
        tMandatoryItems = float(totalMandatoryItems)
        grand_total = gran_total_smart_display + tMandatoryItems

        if (quantityMandatoryItems <= 500):
            grand_total_formatted = "{:,.3f}".format(grand_total)
            contenido_pdf += f"""
            <div class="grand-total">
                <table>
                    <tr>
                        <th class="feauture-total">Grand Total:</th>
                        <td class="feauture-total"><strong>$ {grand_total_formatted}</strong></td>
                    </tr>
                </table>
            </div>
            """
        else:
            print("d%: ", calcular_descuento_por_lotes(quantityMandatoryItems))
            discountGet = calcular_descuento_por_lotes(quantityMandatoryItems)
            discount = grand_total * discountGet
            grand_total_discount = grand_total - discount
            grand_total_discount_formatted = "{:,.3f}".format(grand_total_discount)
            discount_formatted = "{:,.3f}".format(discount)
            contenido_pdf += f"""

            <div class="grand-total">
                <table>
                    <tr>
                        <th class="feauture-total">Discount:</th>
                        <td class="feauture-total"><strong>-$ {discount_formatted}</strong></td>
                    </tr>
                </table>
            </div>
            <div class="grand-total">
                <table>
                    <tr>
                        <th class="feauture-total">Grand Total:</th>
                        <td class="feauture-total"><strong>$ {grand_total_discount_formatted}</strong></td>
                    </tr>
                </table>
            </div>
            """

        contenido_pdf += '</div></body></html>'

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