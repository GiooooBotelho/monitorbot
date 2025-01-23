import numpy as np
from config import period

def calculate_rsi(closes, period=period):
    """
    Calcula o Índice de Força Relativa (RSI) para uma lista de preços de fechamento.
    Args:
        closes (list): Lista de preços de fechamento.
        period (int): Número de períodos a considerar para o cálculo.
    Returns:
        float: Valor do RSI.
    """
    deltas = np.diff(closes)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.average(gain[-period:])
    avg_loss = np.average(loss[-period:])

    if avg_loss == 0:
        rs = float('inf')  # Definir RS como infinito se avg_loss é 0
    else:
        rs = avg_gain / avg_loss
    
    rsi = 100 - (100 / (1 + rs))
    return rsi
