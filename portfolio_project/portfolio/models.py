from django.db import models
import yfinance as yf
from datetime import datetime, timedelta
import random

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)  # Ticker de la acción

    def get_price(self, date):
        # Convertir la fecha a objeto datetime
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        today = datetime.now()

        # Verificar si la fecha es futura
        if date_obj > today:
            print(f"No hay datos para fechas futuras: {date}")
            return 0

        # Usa yfinance para obtener los precios históricos
        stock_data = yf.Ticker(self.symbol)
        try:
            # Agregar un día a la fecha de fin porque 'end' es exclusivo en yfinance
            next_day = date_obj + timedelta(days=1)
            historical_data = stock_data.history(start=date_obj.strftime('%Y-%m-%d'), end=next_day.strftime('%Y-%m-%d'))

            if not historical_data.empty:
                # Retorna el precio de cierre ajustado
                return historical_data['Close'][0]
            else:
                # Si no hay datos en la fecha exacta, buscar el precio más cercano anterior
                past_date = date_obj - timedelta(days=7)  # Buscar en los últimos 7 días
                historical_data = stock_data.history(start=past_date.strftime('%Y-%m-%d'), end=date_obj.strftime('%Y-%m-%d'))

                if not historical_data.empty:
                    # Obtener el último precio disponible antes de la fecha solicitada
                    return historical_data['Close'][-1]
                else:
                    print(f"No se encontraron datos para {self.symbol} en el rango de fechas.")
                    return 0  # No hay datos disponibles
        except Exception as e:
            # Manejar posibles errores
            print(f"Error al obtener datos para {self.symbol}: {e}")
            return 0


class Portfolio(models.Model):
    stocks = models.ManyToManyField(Stock, through='PortfolioStock')
    start_date = models.DateField()
    end_date = models.DateField()

    def calculate_profit(self):
        profit = 0
        for portfolio_stock in self.portfoliostock_set.all():
            start_price = portfolio_stock.stock.get_price(self.start_date.strftime('%Y-%m-%d'))
            end_price = portfolio_stock.stock.get_price(self.end_date.strftime('%Y-%m-%d'))
            if start_price and end_price:
                profit += (end_price - start_price) * portfolio_stock.percentage / 100
        return profit

    def annualized_return(self):
        profit = self.calculate_profit()
        duration = (self.end_date - self.start_date).days / 365.25
        if duration > 0:
            return (profit / duration)
        return 0

class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    percentage = models.FloatField()  # Porcentaje del portafolio asignado a esta acción
