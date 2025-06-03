from datetime import datetime
import random
from config.constants import SEVERIDADES, TEMPOS_SEVERIDADE


def calcular_tempo_estimado(severidade):
    """Calcula tempo estimado baseado na severidade"""
    if severidade in TEMPOS_SEVERIDADE:
        min_tempo, max_tempo = TEMPOS_SEVERIDADE[severidade]
        return random.randint(min_tempo, max_tempo)
    return 60


def obter_nome_severidade(severidade_num):
    """Converte número da severidade para nome"""
    return SEVERIDADES.get(severidade_num, "DESCONHECIDA")


def validar_entrada_numerica(entrada, min_val=1, max_val=4):
    """Valida entrada numérica dentro de um range"""
    try:
        valor = int(entrada)
        return min_val <= valor <= max_val
    except ValueError:
        return False
    except TypeError:
        return False


def limpar_tela():
    """Limpa a tela do terminal"""
    import os

    os.system("cls" if os.name == "nt" else "clear")


def datetime_para_str(obj):
    """Converte objetos datetime para string ISO 8601 para serialização JSON."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Objeto {obj} não é serializável por padrão")
