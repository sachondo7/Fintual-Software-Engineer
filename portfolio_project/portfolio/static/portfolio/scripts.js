function togglePercentage(stockId) {
    // Obtener la checkbox y el campo de porcentaje correspondientes
    var checkbox = document.getElementById('stock_' + stockId);
    var percentageField = document.getElementById('percentage_' + stockId);

    // Si la checkbox está marcada, habilitar el campo de porcentaje, si no, deshabilitarlo
    if (checkbox.checked) {
        percentageField.disabled = false;
    } else {
        percentageField.disabled = true;
        percentageField.value = '';  // Limpiar el valor si se deshabilita
    }
}

// Función para obtener la fecha actual en formato YYYY-MM-DD
function getTodayDate() {
    return new Date().toISOString().split('T')[0];
}

// Función para mostrar el mensaje de error si se selecciona una fecha futura
function showDateErrorMessage(fieldName) {
    var errorMessageDiv = document.getElementById('date-error-message');
    errorMessageDiv.style.display = 'block';
    errorMessageDiv.innerHTML = `<p>El sistema utiliza precios reales de las acciones, por lo tanto, debes seleccionar una fecha anterior o igual a la actual para el campo ${fieldName}.</p>`;
}

// Función para verificar si la fecha seleccionada es futura
function checkFutureDate(date, fieldName) {
    var today = getTodayDate();
    if (date > today) {
        showDateErrorMessage(fieldName);
        return false;
    }
    document.getElementById('date-error-message').style.display = 'none';  // Esconder el mensaje si la fecha es válida
    return true;
}

// Función para obtener precios usando AJAX
function getPricesForDates() {
    var startDate = document.getElementById('start_date').value;
    var endDate = document.getElementById('end_date').value;

    // Verificar si las fechas son futuras
    if (!checkFutureDate(startDate, 'Fecha de inicio') || !checkFutureDate(endDate, 'Fecha de fin')) {
        return;  // No continuar si alguna fecha es futura
    }

    var stockIds = document.querySelectorAll('input[name="stocks[]"]:checked');  // Obtener los IDs de las acciones seleccionadas

    if (startDate && endDate) {
        // Iterar sobre las acciones seleccionadas y obtener los precios
        stockIds.forEach(function(stockCheckbox) {
            var stockId = stockCheckbox.value;

            // Realizar una llamada AJAX para obtener los precios de inicio y fin
            fetch(`/get_stock_prices/?stock_id=${stockId}&start_date=${startDate}&end_date=${endDate}`)
                .then(response => response.json())
                .then(data => {
                    // Actualizar los campos de precio en el frontend
                    document.getElementById(`start_price_${stockId}`).innerText = data.start_price || 'N/A';
                    document.getElementById(`end_price_${stockId}`).innerText = data.end_price || 'N/A';
                })
                .catch(error => {
                    console.error('Error al obtener precios:', error);
                });
        });
    }
}

// Llamar a la función cuando se cambien las fechas
document.getElementById('start_date').addEventListener('change', getPricesForDates);
document.getElementById('end_date').addEventListener('change', getPricesForDates);
