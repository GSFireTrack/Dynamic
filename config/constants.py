DEBUG = True

DELAY_TIME = 0.1  # Tempo de delay entre ações

SEVERIDADES = {1: "BAIXA", 2: "MEDIA", 3: "ALTA", 4: "CRITICA"}

TEMPOS_SEVERIDADE = {
    1: (30, 60),  # BAIXA
    2: (60, 120),  # MEDIA
    3: (120, 240),  # ALTA
    4: (240, 480),  # CRITICA
}

STATUS_OCORRENCIA = {
    "PENDENTE": "Pendente",
    "EM_ANDAMENTO": "Em Andamento",
    "CONCLUIDA": "Concluída",
    "CANCELADA": "Cancelada",
}

EQUIPES_DISPONIVEIS = ["Equipe Alpha", "Equipe Beta", "Equipe Gamma", "Equipe Delta"]

REGIOES_PADRAO = [
    "Cerrado Norte",
    "Mata Atlântica",
    "Pantanal Sul",
    "Amazônia Oeste",
    "Caatinga Leste",
    "Pampa Central",
    "Cerrado Sul",
    "Floresta Urbana",
]

DESCRICOES_PADRAO = [
    "Incêndio em vegetação seca",
    "Queimada atingindo área residencial",
    "Foco de incêndio em mata preservada",
    "Queimada próxima a rodovia",
    "Incêndio em área de pastagem",
    "Fogo em unidade de conservação",
    "Incêndio em área urbana",
    "Queimada em área de reflorestamento",
    "Incêndio em área de proteção ambiental",
    "Fogo em área de cultivo agrícola",
    "Incêndio em área de mineração",
]
