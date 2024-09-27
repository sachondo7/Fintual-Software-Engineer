from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_portfolio, name='create_portfolio'),
    path('summary/<int:portfolio_id>/', views.portfolio_summary, name='portfolio_summary'),
    path('get_stock_prices/', views.get_stock_prices, name='get_stock_prices'),
]
