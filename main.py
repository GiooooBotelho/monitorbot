import asyncio
import sys
from binance import AsyncClient
from config import mainnet_api_key, mainnet_secret_key, interval, period, limit, bot_token, chat_id
from trading_functions import calculate_rsi
from binance_api import get_closes, get_klines # Alterado para buscar dados das velas em binance_api
from telegram_integration import send_telegram_message
import pandas as pd
from pathlib import Path
from datetime import datetime # Importando o módulo datetime

async def fetch_price_and_rsi(symbol):
    """
    Retorna o preço atual e o RSI para o símbolo especificado, exibe no console, e envia para o telegram a cada 30 minutos.
    """
    client = await AsyncClient.create(mainnet_api_key, mainnet_secret_key)
    
    try:
        while True:
            # Obtém o preço atual
            ticker = await client.get_symbol_ticker(symbol=symbol)
            current_price = float(ticker['price'])

            # Obtém os dados de fechamento para calcular o RSI
            closes = await get_closes(client, symbol, interval, limit)
            rsi = calculate_rsi(closes, period)
            
            #pega o preço do candle de 24h atrás para usar na variação
            try:
                klines_24h = await get_klines(client, symbol, interval, 2) #pega o preço de fechamento do candle de 24h atras em ms, e o atual
                if klines_24h and len(klines_24h) >= 2:  # Para evitar erros do codigo caso ele nao consiga pegar os dados
                    price_24h = float(klines_24h[-2][4]) if klines_24h else 0  # o valor que queremos para usar no calculo é o candle anterior ao atual
                    variation_24h = ((current_price - price_24h) / price_24h) * 100 # calcula variacao percentual de preço nas ultimas 24 horas
                else:
                    price_24h = 0  # Caso a api de problema ou algo de errado, seta para 0
                    variation_24h = 0 # seta como zero também
            
            except Exception as e: # caso de algum erro, os valores devem continuar como 0 pra que o programa não quebre
                price_24h = 0
                variation_24h = 0
                print(f"\nErro ao buscar dados para variação de 24h: {e}")

            # Formata a mensagem para enviar pro telegram  
            formatted_message = format_telegram_message(symbol, current_price, rsi, interval, variation_24h)
            
             # Imprime as informações no console
            sys.stdout.write(
                f"\rPreço Atual de {symbol}: \033[1;36m${current_price:.2f}\033[0m | RSI Atual ({interval}): \033[1;36m{rsi:.2f}\033[0m | Variação (24h): \033[1;36m{variation_24h:.2f}%\033[0m"
            )
            sys.stdout.flush()
            
            # Envia informações para o telegram
            send_telegram_message(bot_token, chat_id, formatted_message) # envia a mensagem

            # Formata os dados e salva em planilha
            data_row = format_monitor_data(symbol, current_price, rsi, variation_24h)
            save_monitor_data_to_excel(data_row)

            await asyncio.sleep(900)  # Espera 15 minutos antes de buscar novamente

    except Exception as e:
        print(f"\nErro ao buscar dados: {e}")
    finally:
        # Fecha a conexão com a API da Binance
        await client.close_connection()

def format_telegram_message(symbol, current_price, rsi, interval, variation_24h):
    """
    Formata a mensagem para o Telegram.
    """
    return f"📈 <b>Preço Atual</b> de <b>{symbol}</b>: <b>${current_price:.2f}</b>\n📊 <b>RSI Atual</b> ({interval}): <b>{rsi:.2f}</b>\n📉 <b>Variação</b> (24h): <b>{variation_24h:.2f}%</b>"

def format_monitor_data(symbol, current_price, rsi, variation_24h):
    """
    Formata os dados coletados pelo monitor para salvar em uma planilha.

    Args:
        symbol (str): Símbolo do ativo.
        current_price (float): Preço atual do ativo.
        rsi (float): Valor do RSI.
        variation_24h (float): Variação percentual do preço nas últimas 24h.

    Returns:
        dict: Dicionário contendo os dados formatados.
    """
    return {
        "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Símbolo": symbol,
        "Preço Atual": current_price,
        "RSI": rsi,
        "Variação 24h": variation_24h
    }

def save_monitor_data_to_excel(data_row):
    """
    Salva os dados do monitor em uma planilha Excel.

    Args:
        data_row (dict): Dicionário contendo os dados a serem salvos.
    """
    filename = "monitor_results.xlsx"
    filepath = Path(__file__).parent / filename  # Salva na mesma pasta do script

    new_row_df = pd.DataFrame([data_row])

    if filepath.exists():
        df = pd.read_excel(filepath)
        df = pd.concat([df, new_row_df], ignore_index=True)
    else:
        df = new_row_df

    df.to_excel(filepath, index=False)

async def main():
    symbol = input("\nDigite o símbolo para monitorar (ex.: BTCUSDT): \033[1;36m").strip().upper()
    print("\033[0m")
  
    price_rsi_task = asyncio.create_task(fetch_price_and_rsi(symbol))

    await asyncio.gather(price_rsi_task) # Monitora apenas a task de preço e RSI

if __name__ == "__main__":
    asyncio.run(main())