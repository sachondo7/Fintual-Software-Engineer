from django.shortcuts import render, redirect
from .models import Stock, Portfolio
from django.http import JsonResponse
from django.contrib import messages

def create_portfolio(request):
    if request.method == 'POST':
        # Recoge los datos enviados desde el formulario
        stocks_data = request.POST.getlist('stocks[]')
        percentages_data = request.POST.getlist('percentages[]')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Convertimos los porcentajes a flotantes y calculamos el total
        total_percentage = sum([float(p) for p in percentages_data])

        # Validamos que el porcentaje total sea 100%
        if total_percentage != 100:
            messages.error(request, 'El porcentaje total debe sumar 100%.')
            stocks = Stock.objects.all()
            return render(request, 'create_portfolio.html', {'stocks': stocks})

        # Si el porcentaje es válido, creamos el portafolio
        portfolio = Portfolio.objects.create(start_date=start_date, end_date=end_date)

        # Añadimos cada acción seleccionada con su porcentaje al portafolio
        all_stocks = Stock.objects.all()  # Obtener todas las acciones disponibles
        for stock in all_stocks:
            if str(stock.id) in stocks_data:
                # Acción seleccionada, usar el porcentaje asignado
                index = stocks_data.index(str(stock.id))
                percentage = float(percentages_data[index])
            else:
                # Acción no seleccionada, asignar porcentaje 0
                percentage = 0

            portfolio.stocks.add(stock, through_defaults={'percentage': percentage})

        # Redirige a la página de resumen del portafolio
        return redirect('portfolio_summary', portfolio_id=portfolio.id)

    # Si es GET, mostramos el formulario con todas las acciones disponibles
    stocks = Stock.objects.all()
    return render(request, 'create_portfolio.html', {'stocks': stocks})

def portfolio_summary(request, portfolio_id):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    profit = 0
    start_date = portfolio.start_date.strftime('%Y-%m-%d')
    end_date = portfolio.end_date.strftime('%Y-%m-%d')
    missing_prices = []  # Lista para guardar las acciones que no se encontraron
    portfolio_composition = []  # Lista para almacenar la composición del portafolio (acciones y porcentajes)

    # Calcular las ganancias de cada acción y obtener la composición del portafolio
    for portfolio_stock in portfolio.portfoliostock_set.all():
        stock = portfolio_stock.stock
        start_price = stock.get_price(start_date)
        end_price = stock.get_price(end_date)

        if start_price == 0 or end_price == 0:
            missing_prices.append(stock.name)
            continue

        # Agregar la acción, su porcentaje, y los precios a la composición del portafolio
        portfolio_composition.append({
            'name': stock.name,
            'symbol': stock.symbol,
            'percentage': portfolio_stock.percentage,
            'start_price': round(start_price, 2),  # Limitar a 2 decimales
            'end_price': round(end_price, 2)  # Limitar a 2 decimales
        })

        # Calcula la ganancia según el porcentaje del portafolio asignado a la acción
        gain = (end_price - start_price) * portfolio_stock.percentage / 100
        profit += gain

    # Calcular el retorno anualizado
    duration = (portfolio.end_date - portfolio.start_date).days / 365.25
    annualized_return = (profit / duration) if duration > 0 else 0

    return render(request, 'portfolio_summary.html', {
        'portfolio': portfolio,
        'profit': round(profit, 2),
        'annualized_return': round(annualized_return, 2),
        'missing_prices': missing_prices,
        'portfolio_composition': portfolio_composition
    })




def get_stock_prices(request):
    stock_id = request.GET.get('stock_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        stock = Stock.objects.get(id=stock_id)
        # Obtener los precios de la acción en las fechas seleccionadas
        start_price = stock.get_price(start_date)
        end_price = stock.get_price(end_date)
    except Stock.DoesNotExist:
        return JsonResponse({'error': 'Stock no encontrado'}, status=404)

    return JsonResponse({
        'start_price': start_price,
        'end_price': end_price
    })

