import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

# Binance API Keys for different environments

# Mainnet - Chaves de API para a versão principal de negociação em Binance.
mainnet_api_key = os.getenv("mainnet_api_key")
mainnet_secret_key = os.getenv("mainnet_secret_key")

# Telegram - Configurações para integração com o bot do Telegram para notificações.
bot_token = os.getenv("bot_token")
chat_id = os.getenv("chat_id")

interval = '1h'  # Intervalo de tempo para buscar dados de velas (candles).
period = 20       # Período utilizado para cálculos que envolvem médias móveis ou outros indicadores.
limit = 50        # Limite de dados históricos (por exemplo, velas) para recuperar de uma vez.