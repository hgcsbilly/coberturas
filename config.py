import bybit
import numpy as np
from config import API_KEY, API_SECRET

# Crear instancia del cliente de Bybit
client = bybit.bybit(test=False, api_key=API_KEY, api_secret=API_SECRET)

def check_open_position(symbol):
    """Verifica si hay una posición abierta para el símbolo dado"""
    positions = client.Positions.Positions_myPosition(symbol=symbol).result()[0]
    for position in positions['result']:
        if position['side'] == 'Buy' and float(position['size']) > 0:
            return position
        elif position['side'] == 'Sell' and float(position['size']) < 0:
            return position
    return None

def place_market_order(symbol, side, quantity):
    """Coloca una orden de mercado para el símbolo dado"""
    order = client.Order.Order_new(symbol=symbol, side=side, order_type='Market', qty=quantity, time_in_force='GoodTillCancel').result()[0]
    return order

def place_limit_order(symbol, side, quantity, price):
    """Coloca una orden límite para el símbolo dado"""
    order = client.Order.Order_new(symbol=symbol, side=side, order_type='Limit', qty=quantity, price=price, time_in_force='GoodTillCancel').result()[0]
    return order

def main():
    symbol = input("¿Qué moneda deseas operar? ")
    position = check_open_position(symbol)
    
    if position:
        coverage_percentage = float(input(f"Tienes una posición abierta. ¿A qué porcentaje deseas la cobertura? "))
        quantity = abs(float(position['size'])) * (coverage_percentage / 100)
        
        # Coloca una orden de mercado contraria a la posición abierta
        if position['side'] == 'Buy':
            place_market_order(symbol, 'Sell', quantity)
        else:
            place_market_order(symbol, 'Buy', quantity)
        
        take_profit_percentage = float(input(f"¿A qué porcentaje deseas tomar ganancias? "))
        take_profit_price = float(position['entry_price']) * (1 + (take_profit_percentage / 100))
        
        # Coloca una orden límite para tomar ganancias
        if position['side'] == 'Buy':
            place_limit_order(symbol, 'Sell', quantity, take_profit_price)
        else:
            place_limit_order(symbol, 'Buy', quantity, take_profit_price)
    else:
        print(f"No hay posiciones abiertas para {symbol}")

if __name__ == "__main__":
    main()