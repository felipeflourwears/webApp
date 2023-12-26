function generarPDFLF() {
    var allBatchData = []; // Obtener datos del Local Storage
    for (var i = 1; i < currentBatch; i++) {
        var storedData = localStorage.getItem('itemsData' + i);
        if (storedData !== null) {
            var parsedData = JSON.parse(storedData);
            allBatchData = allBatchData.concat(parsedData);
        }
    }

    // Enviar solicitud al backend para generar el PDF
    fetch('/generar_pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ datos: allBatchData })
    })
    .then(response => {
        // Manejar la respuesta del servidor (por ejemplo, descargar el PDF)
        if (response.ok) {
            return response.blob().then(blob => {
                const url = window.URL.createObjectURL(new Blob([blob]));
                const a = document.createElement('a');
                a.href = url;
                a.download = 'mi_pdf.pdf';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
        } else {
            // Manejar errores de la respuesta
            console.error('Error al generar el PDF');
        }
    })
    .catch(error => {
        // Manejar errores de la solicitud
        console.error('Error al generar el PDF:', error);
    });
}


var currentBatch = 1; // Inicializar el contador de lotes
var preciosPorSeleccion = {
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
};

//Prices
var video_procesor = 377.988;
var freight_import_taxes = 487.20;
var install = 931.02;
var cms = 152.1;
var noc = 720;
var totalFixed;

// Calcular la suma de los precios
totalFixed = video_procesor + freight_import_taxes + install + cms + noc;


$(document).ready(function() {

    function updateDataDisplay() {
        
        var dataDisplay = $('#dataDisplay');
        var totalPriceDisplay = $('#totalPriceDisplay'); // Obtener el div para mostrar el precio total
        var totalAllBatchesPrice = 0; // Inicializar el precio total de todos los lotes
        var cantidadLotes = 0; // Inicializar la cantidad de lotes
        
        
        dataDisplay.empty(); // Limpiar el contenido actual
        totalPriceDisplay.empty();

        

        for (var i = 1; i < currentBatch; i++) {
            var storedData = JSON.parse(localStorage.getItem('itemsData' + i));
            cantidadLotes++;

            if (storedData !== null) { // Verificar si storedData no es nulo
                var totalPricePerBatch = 0; // Inicializar el precio total del lote actual

                var table = $('<table></table>').addClass('batch-table');


                // Calcular el precio total del lote actual
                storedData.forEach(function(item) {
                    var itemKey = item.size;
                    console.log("DEBUG: ", itemKey)
                    console.log("Boolean: ",preciosPorSeleccion.hasOwnProperty(itemKey))
                    if (preciosPorSeleccion.hasOwnProperty(itemKey)) {
                        var pricePerItem = preciosPorSeleccion[itemKey];
                        console.log("Price: ", preciosPorSeleccion[itemKey])
                        var totalForItem = pricePerItem * item.quantity;
                        totalPricePerBatch += totalForItem;
                    }
                });

                // Agregar el total fijo al precio total del lote actual
                totalPricePerBatch += totalFixed;

                // Actualizar el total de todos los lotes sumados
                totalAllBatchesPrice += totalPricePerBatch;

                // Crear la cabecera de la tabla
                var thead = $('<thead><tr><th colspan="8">OPTION ' + i + '</th></tr></thead>');
                table.append(thead);

                var thead = $('<thead><tr>' +
                '<th>Product</th>' +
                '<th>Size</th>' +
                '<th>Quantity</th>' +
                '<th>Price per Item</th>' +
                '<th>Total price &nbsp; &nbsp; <button class="btn delete-batch-btn btn-danger" data-batch="' + i + '"><i class="bi bi-trash"></i></button></th>' +
                '</tr></thead>');

                table.append(thead);



                var tbody = $('<tbody></tbody>');

                // Crear filas para cada elemento en el lote
                storedData.forEach(function(item) {
                    var row = $('<tr></tr>');
                    for (var key in item) {
                        if (item.hasOwnProperty(key)) {
                        
                            if (item[key].indexOf("Pitch") !== -1) {
                                var stringWithoutLastFive = item[key].slice(0, -6);
                                row.append('<td>' + stringWithoutLastFive + '</td>');
                            }else{
                                row.append('<td>' + item[key] + '</td>');
                            }
                        }
                    }

                    // Agregar columna para el precio total por tipo y tamaño
                    var itemKey = item.size;
                    
                    if (preciosPorSeleccion.hasOwnProperty(itemKey)) {
                        var pricePerItem = preciosPorSeleccion[itemKey];
                        var totalForItem = pricePerItem * item.quantity;

                        // Formatear los números con comas como separadores de miles
                        var formattedPricePerItem = pricePerItem.toLocaleString('en-US');
                        var formattedTotalForItem = totalForItem.toLocaleString('en-US');

                        row.append('<td> $ ' + formattedPricePerItem + '</td>');
                        row.append('<td><strong>$ ' + formattedTotalForItem + '</strong></td>');
                    }

                    tbody.append(row);
                });

                table.append(tbody);
                dataDisplay.append(table);
            }
        }
       
    }



    // Función para eliminar un lote al hacer clic en el botón "Delete Batch"
    $(document).on('click', '.delete-batch-btn', function() {
        var batchNumber = $(this).data('batch');
        var confirmation = confirm('Are you sure delete this batch ' + batchNumber + '?');

        if (confirmation) {
            localStorage.removeItem('itemsData' + batchNumber);
            updateDataDisplay();
        }
    });


    $('#addToListBtn').click(function() {
        var headerItems = $('.headers-container .row');
        var shielfItems = $('.shielfs-container .row');
        var currentBatchItems = []; // Array para el lote actual
        var itemsByTypeAndSize = {};

        headerItems.each(function() {
            var headerSize = $(this).find('select[name="headerSize"]').val();
            var headerSizePi = $(this).find('select[name="headerSizePi"]').val();
            var quantity = $(this).find('input[name="quantity"]').val();
            var key = 'Pitch'+ ' '+ headerSizePi + ' '+ headerSize + ' '  + 'Header'; 
            console.log("Key Header: ", key)
            // Almacenar el artículo en la estructura de datos itemsByTypeAndSize
            if (!itemsByTypeAndSize[key]) {
                itemsByTypeAndSize[key] = {
                    type: 'Header',
                    size: key,
                    quantity: 0
                };
            }
            itemsByTypeAndSize[key].quantity += parseInt(quantity); // Actualizar la cantidad

            currentBatchItems.push({
                type: 'Header',
                size: key,
                quantity: quantity
            });
        });

        shielfItems.each(function() {
            var shielfSize = $(this).find('select[name="shielfSize"]').val();
            var piShielf = $(this).find('select[name="piShielf"]').val();
            var quantity = $(this).find('input[name="quantity"]').val();
            var key = 'Pitch'+ ' '+ piShielf + ' '+ shielfSize + ' ' + 'Shelf'; // Generar clave de tipo y tamaño
            console.log("key shelf:  ", key)
            // Almacenar el artículo en la estructura de datos itemsByTypeAndSize
            if (!itemsByTypeAndSize[key]) {
                itemsByTypeAndSize[key] = {
                    type: 'Shelf',
                    size: key,
                    quantity: 0
                };
            }
            itemsByTypeAndSize[key].quantity += parseInt(quantity); // Actualizar la cantidad

            currentBatchItems.push({
                type: 'Shelf',
                size: key,
                quantity: quantity
            });
        });

        var totalQuantity = $('input[name="cantidad"]').val(); // Obtener el valor del input 'Total Quantity'

        // Calcula el valor total multiplicando totalQuantity por totalFixed
        const totalValue = totalQuantity * totalFixed;

        // Formatea totalQuantity como cantidad sin símbolo de dólar
        const formattedTotalQuantity = totalQuantity.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
        });

        // Formatea el valor total como cantidad monetaria
        const formattedTotalValue = '$' + totalValue.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
        });

        // Crea la cadena con el formato deseado
        const formattedSize = `${formattedTotalValue}`;

        // Agregar el valor de 'Total Quantity' al objeto currentBatchItems
        currentBatchItems.push({
            type: 'Mandatory KITS',
            size: formattedSize,
            quantity: totalQuantity,
        });

         // Restablecer el valor del input a '1' para el próximo lote
        $('input[name="cantidad"]').val('1');


        // Guardar el lote actual en localStorage con una clave diferente para cada lote
        localStorage.setItem('itemsData' + currentBatch, JSON.stringify(currentBatchItems));
        console.log('Lote ' + currentBatch + ': ', currentBatchItems);

        currentBatch++; // Incrementar el contador para el próximo lote
        updateDataDisplay(); // Actualizar la visualización de los datos


        var headerItems = $('.headers-container .row');
        var shielfItems = $('.shielfs-container .row');

        // Restablecer los campos de entrada en headers-container y shielfs-container
        $('.headers-container').empty();
        $('.shielfs-container').empty();

        // Calcular el precio total por lote
        var totalPricePerLote = totalFixed;
        currentBatchItems.forEach(function(item) {
            var key = item.size;
            if (preciosPorSeleccion.hasOwnProperty(key)) {
                totalPricePerLote += preciosPorSeleccion[key] * item.quantity;
            }
        });

        // Verificar si los datos del localStorage están disponibles antes de llamar a generarPDF
        //generarPDF();

    });

    // Mostrar los datos al cargar la página
    updateDataDisplay();
});


