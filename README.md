<p align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GSFireTrack/.github/main/utils/logo/logoDarkHD.png">
        <img alt="Logo da FireTrack" src="https://raw.githubusercontent.com/GSFireTrack/.github/main/utils/logo/logoHD.png" width="300">
    </picture>
</p>

# 🔥 Simulador de Resposta a Queimadas

Um sistema de simulação para gerenciamento de resposta a incêndios e queimadas, implementado usando estruturas de dados fundamentais em Python.

<details open>
    <summary><h3><strong>📑 Sumário</strong></h3>
        <ol>
            <li><a href="#info">Informações</a></li>
            <li><a href="#visao-geral">Visão Geral</a></li>
            <li><a href="#estrutura-do-projeto">Estrutura do Projeto</a></li>
            <li><a href="#principais-recursos">Principais Recursos</a></li>
            <li><a href="#como-executar">Como Executar</a></li>
            <li><a href="#estruturas-de-dados-utilizadas">Estruturas de Dados Utilizadas</a></li>
            <li><a href="#exemplos-de-uso">Exemplos de Uso</a></li>
            <li><a href="#configuracoes">Configurações</a></li>
            <li><a href="#recursos-futuros">Recursos Futuros</a></li>
        </ol>
    </summary>
</details>

<h2 id="info"> ℹ️ Informações </h2>

<table>
  <tr>
    <td><strong>Organização Github</strong></td>
    <td><a href="https://github.com/GSFireTrack">GSFireTrack</a></td>
  </tr>
  <tr>
    <td><strong>Curso</strong></td>
    <td>Engenharia de Software</td>
  </tr>
  <tr>
    <td><strong>Disciplina</strong></td>
    <td>Dynamic Programming</td>
  </tr>
   <tr>
      <td><strong>Professor</strong></td>
      <td>Prof. Lucas Mendes Marques Gonçalves</td>
   </tr>
  <tr>
    <td><strong>Turma</strong></td>
    <td>2ESPX</td>
  </tr>
</table>

<h2 id="equipe"> 👥 Equipe </h2>

| Integrante                      | RM     |
| ------------------------------- | ------ |
| Augusto Barcelos Barros         | 565065 |
| Jefferson Junior Alvarez Urbina | 558497 |

<h2 id="visao-geral">📋 Visão Geral</h1>

Este projeto demonstra a implementação prática de estruturas de dados clássicas aplicadas a um problema real: o gerenciamento de emergências de combate a incêndios. O sistema utiliza diferentes estruturas para otimizar operações específicas:

- [x] **Heap (Fila de Prioridade)**: Gerencia ocorrências pendentes por prioridade baseada na severidade
- [x] **Pilha (Stack)**: Controla histórico de configurações para desfazer última ação no config manager
- [x] **Fila (Queue)**: Gerencia ocorrências aguardando equipes disponíveis com processamento automático
- [x] **Lista Ligada**: Mantém histórico cronológico de todas as ações do sistema
- [x] **Árvore Binária de Busca**: Organiza e busca ocorrências por região geográfica

<h2 id="estrutura-do-projeto">📁 Estrutura do Projeto</h2>

```
simulador_queimadas/
├── main.py                  # Arquivo principal com menu interativo
├── config/
│   ├── config_manager.py    # Gerenciador de configurações com histórico (pilha)
│   └── constants.py         # Constantes e configurações do sistema
├── data/
│   └── ocorrencias.json     # Armazenamento de ocorrências (JSON)
├── interfaces/
│   └── console.py           # Instância de console para Rich
│   ├── menu.py              # Interface de menu e seleção modular de ocorrências
├── models/
│   └── ocorrencia.py        # Modelo de dados da ocorrência
├── structures/
│   └── arvore_regioes.py    # Implementação da árvore binária
│   ├── fila.py              # Implementação da fila (FIFO)
│   ├── heap_prioridade.py   # Implementação do heap para prioridades
│   ├── lista_ligada.py      # Implementação da lista ligada
│   ├── pilha.py             # Implementação da pilha (LIFO)
├── services/
│   ├── persistence.py       # Serviço de persistência de dados
│   └── simulador.py         # Lógica do simulador
└── utils/
    └── helpers.py           # Funções auxiliares e utilitários
```

<h2 id="principais-recursos">🎯 Principais Recursos</h2>

1. **Gestão de Ocorrências por Prioridade**

   - Criação de novas ocorrências com severidade (Baixa, Média, Alta, Crítica)
   - Atendimento automático baseado em prioridade e ordem cronológica
   - Cálculo automático de tempo estimado baseado na severidade

2. **Controle de Equipes**

   - Gerenciamento de equipes disponíveis e ocupadas
   - Atribuição automática de equipes às ocorrências
   - Sistema de dicionário para mapear equipe-ocorrência em andamento
   - Processamento automático da fila de espera quando equipes ficam disponíveis
   - Movimentação automática de ocorrências para fila de espera quando não há equipes disponíveis

3. **Histórico Completo**

   - Registro cronológico de todas as ações do sistema
   - Busca por ocorrência específica
   - Visualização das últimas N ações

4. **Relatórios por Região**

   - Organização geográfica das ocorrências
   - Estatísticas por região em ordem alfabética
   - Contadores por status (Pendente, Em Andamento, Concluída)

5. **Simulação Automática**
   - Geração de ocorrências aleatórias para testes
   - Severidades progressivas para cenários realistas
   - Regiões e descrições variadas

<h2 id="como-executar">🚀 Como Executar</h2>

### Pré-requisitos

- Python 3.6 ou superior
- Biblioteca Rich (para interface de terminal)

### Instalação e Execução

1. **Clone ou baixe o projeto**

```bash
# Se usando git
git clone https://github.com/GSFireTrack/Dynamic
cd simulador_queimadas

# Ou simplesmente extraia os arquivos em uma pasta
```

2. **Execute o programa principal**

```bash
python main.py
```

3. **Instale dependências (se necessário)**

   - Se você não tiver a biblioteca Rich instalada, execute:

```bash
pip install rich
```

3. **Navegue pelo menu interativo**

```
🔥 SIMULADOR DE RESPOSTA A QUEIMADAS 🔥
========================================
1.  📝 Inserir nova ocorrência
2.  🚒 Atender próxima ocorrência
3.  ✅ Finalizar atendimento
4.  📋 Listar ocorrências pendentes
5.  ⏳ Listar fila de espera
6.  🔄 Listar ocorrências em andamento
7.  📝 Ver histórico de ações
8.  📊 Relatório por região
9.  🎲 Simular chamadas aleatórias
10. 📈 Status do sistema
11. ⚙️ Configurações do simulador
0.  🚪 Sair
```

<h2 id="exemplos-de-uso">🧪 Exemplos de Uso</h2>

0. **Sair**

   - Escolha opção `0` para sair do simulador
   - O programa será encerrado
   - Os dados serão salvos automaticamente no arquivo [`data/ocorrencias.json`](data/ocorrencias.json)
   - As configurações serão salvas no arquivo [`config/config.json`](config/config.json)

1. **Inserir nova ocorrência**:

   - Escolha opção `1` para criar uma nova ocorrência
   - Informe severidade (Baixa, Média, Alta, Crítica), região e descrição
   - A ocorrência será adicionada à fila de prioridade (Heap)

2. **Atender próxima ocorrência**:

   - Escolha opção `2` para atender a próxima ocorrência
   - Uma equipe será automaticamente atribuída (se disponível)
   - A ocorrência será removida da fila de prioridade e mapeada no dicionário de atendimentos
   - Caso não haja equipes disponíveis, a ocorrência será movida automaticamente para a fila de espera

3. **Finalizar atendimento**:

   - Escolha opção `3` para finalizar uma ocorrência em andamento (seleção interativa)
   - A equipe ficará disponível novamente
   - O sistema processará automaticamente a fila de espera, atribuindo a próxima ocorrência disponível

4. **Listar ocorrências pendentes**:

   - Escolha opção `4` para ver a lista ordenada por prioridade
   - Observe que ocorrências críticas aparecem primeiro

5. **Listar fila de espera**:

   - Escolha opção `5` para ver as ocorrências que aguardam equipe
   - Mostra a lista de ocorrências em espera, ordenadas por ordem de chegada (FIFO)

6. **Listar ocorrências em andamento**:

   - Escolha opção `6` para ver as ocorrências que estão sendo atendidas
   - Mostra a equipe ocupada e o tempo restante estimado

7. **Ver histórico de ações**:

   - Escolha opção `7` para ver o histórico de ações
   - Você pode buscar por uma ocorrência específica ou ver as últimas N ações

8. **Relatório por região**:

   - Escolha opção `8` para relatório por região
   - Veja ocorrências organizadas por região geográfica

9. **Simular chamadas aleatórias**:

   - Escolha opção `9` para gerar 5 ocorrências aleatórias
   - O sistema criará ocorrências com dados aleatórios (severidade, região, descrição)

10. **Status do sistema**:

    - Escolha opção `10` para ver resumo do sistema
    - Observe equipes ocupadas e estatísticas gerais

11. **Configurações do simulador**:

    - Escolha opção `11` para acessar configurações
    - Modifique parâmetros como tema, delay e debug
    - Desfazer última ação no menu (Pilha)
    - Redefina todas as configurações para os valores padrão
    - Exclua todas as ocorrências

<h2 id="estruturas-de-dados-utilizadas">🎲 Estruturas de Dados Utilizadas</h2>

### 1. **Heap (Fila de Prioridade)**

- **Localização**: [`structures/heap_prioridade.py`](structures/heap_prioridade.py)
- **Uso**: Gerencia ocorrências pendentes ordenadas por severidade e timestamp
- **Complexidade**: O(log n) para inserção e remoção

### 2. **Pilha (Stack)**

- **Localização**: [`structures/pilha.py`](structures/pilha.py)
- **Uso**: Armazena histórico de configurações para permitir desfazer últimas ações
- **Complexidade**: O(1) para empilhar e desempilhar configurações

### 3. **Fila (Queue)**

- **Localização**: [`structures/fila.py`](structures/fila.py)
- **Uso**: Armazena ocorrências que aguardam liberação de equipe com processamento automático
- **Complexidade**: O(1) para enfileirar e desenfileirar

### 4. **Lista Ligada**

- **Localização**: [`structures/lista_ligada.py`](structures/lista_ligada.py)
- **Uso**: Mantém histórico cronológico de ações
- **Complexidade**: O(1) para inserção no início, O(n) para busca

### 5. **Árvore Binária de Busca**

- **Localização**: [`structures/arvore_regioes.py`](structures/arvore_regioes.py)
- **Uso**: Organiza ocorrências por região geográfica
- **Complexidade**: O(log n) para busca, inserção (caso médio)

<h2 id="configuracoes">⚙️ Configurações</h2>

Você pode modificar as configurações em [`config/config.json`](config/config.json) ou modificar as constantes em [`config/constants.py`](config/constants.py)

- **DEBUG**: Ativa/Desativa logs de depuração
- **DELAY_TIME**: Tempo de espera entre ações (em segundos)
- **SEVERIDADES**: Lista de severidades possíveis
- **TEMPOS_SEVERIDADE**: Tempos estimados por nível de severidade
- **EQUIPES_DISPONIVEIS**: Lista de equipes de combate
- **REGIOES_PADRAO**: Regiões geográficas disponíveis
- **DESCRICOES_PADRAO**: Descrições usadas na simulação

<h2 id="recursos-futuros">🚧 Recursos Futuros</h2>

Recursos possíveis para futuras versões do simulador:

- [x] Persistência de dados em arquivo/banco (Falta histórico de ações)
- [x] Arquitetura modular com separação de responsabilidades
- [x] Sistema automático de fila de espera
- [ ] API REST usando Flask/FastAPI
- [ ] Mapas interativos das regiões
- [ ] Métricas de performance das equipes
- [ ] Testes unitários automatizados
- [ ] Interface gráfica (GUI)
