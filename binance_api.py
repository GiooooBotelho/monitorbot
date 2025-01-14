from config import interval, limit

async def get_closes(client, symbol, interval=interval, limit=limit): # 🟣🟣
    """
    Obtém os preços de fechamento de velas para um símbolo específico.
    Args:
        client (BinanceAsyncClient): O cliente conectado à API da Binance.
        symbol (str): O símbolo de trading.
        interval (str): O intervalo das velas (ex.: '15m').
        limit (int): O número de velas a ser recuperado.
    Returns:
        list: Uma lista dos preços de fechamento das velas.
    """
    klines = await client.get_klines(symbol=symbol, interval=interval, limit=limit)
    closes = [float(kline[4]) for kline in klines]
    return closes
    
async def get_klines(client, symbol, interval, limit):
    """
    Obtém as informações completas de velas para um símbolo específico.
    Args:
        client (BinanceAsyncClient): O cliente conectado à API da Binance.
        symbol (str): O símbolo de trading.
        interval (str): O intervalo das velas.
         limit (int): O número de velas a ser recuperado.
    Returns:
       list: Os detalhes de vela do ativo (lista de velas, cada vela tem open, close, high, low, volume)
    """
    klines = await client.get_klines(symbol=symbol, interval=interval, limit=limit)
    return klines