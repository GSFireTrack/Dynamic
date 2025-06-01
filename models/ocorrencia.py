from datetime import datetime
from config.constants import STATUS_OCORRENCIA


def criar_ocorrencia(id_ocorrencia, regiao, severidade, descricao, tempo_estimado):
    """Cria uma nova ocorrência"""
    return {
        "id": id_ocorrencia,
        "regiao": regiao,
        "severidade": severidade,
        "descricao": descricao,
        "timestamp": datetime.now(),
        "status": STATUS_OCORRENCIA["PENDENTE"],
        "equipe_atribuida": None,
        "tempo_estimado": tempo_estimado,
    }


def atualizar_status_ocorrencia(ocorrencia, novo_status):
    """Atualiza o status de uma ocorrência"""
    ocorrencia["status"] = novo_status
    return ocorrencia


def atribuir_equipe_ocorrencia(ocorrencia, equipe):
    """Atribui uma equipe à ocorrência"""
    ocorrencia["equipe_atribuida"] = equipe
    return ocorrencia


def comparar_prioridade_ocorrencias(ocorrencia1, ocorrencia2):
    """Compara prioridade entre duas ocorrências para o heap"""
    if ocorrencia1["severidade"] != ocorrencia2["severidade"]:
        return ocorrencia1["severidade"] > ocorrencia2["severidade"]
    return ocorrencia1["timestamp"] < ocorrencia2["timestamp"]


def obter_info_ocorrencia(ocorrencia):
    """Retorna informações formatadas da ocorrência"""
    return {
        "id": ocorrencia["id"],
        "regiao": ocorrencia["regiao"],
        "severidade": ocorrencia["severidade"],
        "descricao": ocorrencia["descricao"],
        "timestamp": ocorrencia["timestamp"].strftime("%d/%m/%Y %H:%M:%S"),
        "status": ocorrencia["status"],
        "equipe_atribuida": ocorrencia["equipe_atribuida"],
        "tempo_estimado": ocorrencia["tempo_estimado"],
    }
