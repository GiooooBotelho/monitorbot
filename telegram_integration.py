import requests

def send_telegram_message(bot_token, chat_id, message):
    """
    Envia uma mensagem para um chat do Telegram usando a API do Telegram.
    Args:
        bot_token (str): O token do bot do Telegram, usado para autenticar a solicitação à API.
        chat_id (str): O ID do chat para o qual a mensagem será enviada.
        message (str): A mensagem a ser enviada.
    Returns:
        dict: Resposta da API do Telegram em formato JSON, contendo detalhes sobre a mensagem enviada ou erro ocorrido.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"  # Adiciona esta linha para ativar o modo HTML
    }
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        print(f"🚨 Erro ao enviar mensagem: {e}")
        return None

# https://api.telegram.org/bot{TOKEN}/getUpdates
