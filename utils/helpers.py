from datetime import datetime
import os
import random
import json
from pathlib import Path
from config.constants import SEVERIDADES, TEMPOS_SEVERIDADE
from structures.arvore_regioes import inserir_arvore
from structures.heap_prioridade import inserir_heap
from structures.pilha import empilhar


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


OCORRENCIAS_FILE_PATH = Path("dados/ocorrencias.json")


def datetime_para_str(obj):
    """Converte objetos datetime para string ISO 8601 para serialização JSON."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Objeto {obj} não é serializável por padrão")


def salvar_ocorrencias_json(simulador, CAMINHO_ARQUIVO=OCORRENCIAS_FILE_PATH):
    """Salva ocorrências no arquivo JSON, convertendo datetime para string."""
    dados = list(simulador["ocorrencias"].values())

    CAMINHO_ARQUIVO.parent.mkdir(parents=True, exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False, default=datetime_para_str)


def carregar_ocorrencias_json(simulador, CAMINHO_ARQUIVO=OCORRENCIAS_FILE_PATH):
    """Carrega ocorrências do arquivo JSON e atualiza estruturas internas do simulador."""
    if not CAMINHO_ARQUIVO.exists():
        return

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for ocorrencia in dados:
        for campo in ["timestamp"]:
            valor = ocorrencia.get(campo)
            if isinstance(valor, str):
                try:
                    ocorrencia[campo] = datetime.fromisoformat(valor)
                except ValueError:
                    ocorrencia[campo] = None

        simulador["ocorrencias"][ocorrencia["id"]] = ocorrencia
        inserir_heap(simulador["fila_prioridade"], ocorrencia)
        inserir_arvore(
            simulador["arvore_regioes"], ocorrencia["regiao"], ocorrencia["id"]
        )

        if ocorrencia["status"] == "Em Andamento":
            empilhar(simulador["pilha_em_andamento"], ocorrencia)
            simulador["equipes_ocupadas"].add(ocorrencia["equipe_atribuida"])


def deletar_ocorrencias_json(CAMINHO_ARQUIVO=OCORRENCIAS_FILE_PATH):
    """Deleta o arquivo de ocorrências JSON."""
    if CAMINHO_ARQUIVO.exists():
        os.remove(CAMINHO_ARQUIVO)
        print(f"Arquivo {CAMINHO_ARQUIVO} deletado com sucesso.")
    else:
        print(f"Arquivo {CAMINHO_ARQUIVO} não encontrado.")
