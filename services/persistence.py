from datetime import datetime
import json
import os
from config.constants import OCORRENCIAS_FILE_PATH
from structures.arvore_regioes import criar_arvore_regioes, inserir_arvore
from structures.heap_prioridade import criar_heap_prioridade, inserir_heap
from structures.lista_ligada import criar_lista_ligada
from structures.pilha import criar_pilha, empilhar
from structures.fila import criar_fila, enfileirar
from utils.helpers import datetime_para_str


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
        inserir_arvore(
            simulador["arvore_regioes"], ocorrencia["regiao"], ocorrencia["id"]
        )

        if ocorrencia["status"] == "Pendente":
            inserir_heap(simulador["fila_prioridade"], ocorrencia)

        if ocorrencia["status"] == "Em Andamento":
            simulador["ocorrencias_em_andamento"][ocorrencia["id"]] = ocorrencia
            if ocorrencia.get("equipe_atribuida"):
                simulador["equipes_ocupadas"].add(ocorrencia["equipe_atribuida"])

        if ocorrencia["status"] == "Em Espera":
            enfileirar(simulador["fila_espera"], ocorrencia)


def deletar_ocorrencias_json(CAMINHO_ARQUIVO=OCORRENCIAS_FILE_PATH):
    """Deleta o arquivo de ocorrências JSON."""
    if CAMINHO_ARQUIVO.exists():
        os.remove(CAMINHO_ARQUIVO)
        print(f"Arquivo {CAMINHO_ARQUIVO} deletado com sucesso.")
    else:
        print(f"Arquivo {CAMINHO_ARQUIVO} não encontrado.")


def simulador_clear(simulador):
    """Limpa o simulador, removendo todas as ocorrências e estruturas internas."""
    simulador["fila_prioridade"] = criar_heap_prioridade()
    simulador["ocorrencias_em_andamento"] = {}
    simulador["historico"] = criar_lista_ligada()
    simulador["arvore_regioes"] = criar_arvore_regioes()
    simulador["fila_espera"] = criar_fila()
    simulador["equipes_ocupadas"] = set()
    simulador["ocorrencias"] = {}
