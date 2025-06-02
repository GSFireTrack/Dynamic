# 🔥 Simulador de Resposta a Queimadas

Um sistema de simulação para gerenciamento de resposta a incêndios e queimadas, implementado usando estruturas de dados fundamentais em Python.

<details open>
    <summary><h3><strong>📑 Sumário</strong></h3>
        <ol>
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

<!-- ## 📋 Visão Geral -->
<h2 id="visao-geral">📋 Visão Geral</h1>

Este projeto demonstra a implementação prática de estruturas de dados clássicas aplicadas a um problema real: o gerenciamento de emergências de combate a incêndios. O sistema utiliza diferentes estruturas para otimizar operações específicas:

- [x] **Heap (Fila de Prioridade)**: Gerencia ocorrências pendentes por prioridade baseada na severidade
- [x] **Pilha (Stack)**: Controla ocorrências em andamento usando LIFO (Last In, First Out)
- [x] **Lista Ligada**: Mantém histórico cronológico de todas as ações do sistema
- [x] **Árvore Binária de Busca**: Organiza e busca ocorrências por região geográfica

<!-- ## 📁 Estrutura do Projeto -->
<h2 id="estrutura-do-projeto">📁 Estrutura do Projeto</h2>

```
simulador_queimadas/
├── main.py                   # Arquivo principal com menu interativo
├── config/
│   └── constants.py          # Constantes e configurações do sistema
├── models/
│   └── ocorrencia.py         # Modelo de dados da ocorrência
├── structures/
│   ├── heap_prioridade.py    # Implementação do heap para prioridades
│   ├── pilha.py              # Implementação da pilha
│   ├── lista_ligada.py       # Implementação da lista ligada
│   └── arvore_regioes.py     # Implementação da árvore binária
├── services/
│   └── simulador_service.py  # Lógica do simulador
└── utils/
    ├── interface_rich.py     # Interface de usuário com Rich
    └── helpers.py            # Funções auxiliares e utilitários
```

<!-- ## 🎯 Principais Recursos -->
<h2 id="principais-recursos">🎯 Principais Recursos</h2>

1. **Gestão de Ocorrências por Prioridade**

   - Criação de novas ocorrências com severidade (Baixa, Média, Alta, Crítica)
   - Atendimento automático baseado em prioridade e ordem cronológica
   - Cálculo automático de tempo estimado baseado na severidade

2. **Controle de Equipes**

   - Gerenciamento de equipes disponíveis e ocupadas
   - Atribuição automática de equipes às ocorrências
   - Controle LIFO para finalização de atendimentos

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
git clone [repositorio]
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
🔥 SIMULADOR DE RESPOSTA A QUEIMADAS
============================================================
1. 📝 Inserir nova ocorrência
2. 🚒 Atender próxima ocorrência
3. ✅ Finalizar atendimento
4. 📋 Listar ocorrências pendentes
5. 🔧 Listar ocorrências em andamento
6. 📝 Ver histórico de ações
7. 📊 Relatório por região
8. 🎲 Simular chamadas aleatórias
9. 📈 Status do sistema
10. ⚙️ Configurações do simulador
0. 🚪 Sair
```

<h2 id="exemplos-de-uso">🧪 Exemplos de Uso</h2>

1. **Inserir nova ocorrência**:

   - Escolha opção `1` para criar uma nova ocorrência
   - Informe severidade (Baixa, Média, Alta, Crítica), região e descrição
   - A ocorrência será adicionada à fila de prioridade (Heap)

2. **Atender próxima ocorrência**:

   - Escolha opção `2` para atender a próxima ocorrência
   - Uma equipe será automaticamente atribuída (se disponível)

3. **Finalizar atendimento**:

   - Escolha opção `3` para finalizar a última ocorrência iniciada
   - A equipe ficará disponível novamente

4. **Listar ocorrências pendentes**:

   - Escolha opção `4` para ver a lista ordenada por prioridade
   - Observe que ocorrências críticas aparecem primeiro

5. **Listar ocorrências em andamento**:

   - Escolha opção `5` para ver as ocorrências que estão sendo atendidas
   - Mostra a equipe ocupada e o tempo restante estimado

6. **Ver histórico de ações**:

   - Escolha opção `6` para ver o histórico de ações
   - Você pode buscar por uma ocorrência específica ou ver as últimas N ações

7. **Relatório por região**:

   - Escolha opção `7` para relatório por região
   - Veja ocorrências organizadas por região geográfica

8. **Simular chamadas aleatórias**:

   - Escolha opção `8` para gerar 5 ocorrências aleatórias
   - O sistema criará ocorrências com dados aleatórios (severidade, região, descrição)

9. **Status do sistema**:

   - Escolha opção `9` para ver resumo do sistema
   - Observe equipes ocupadas e estatísticas gerais

10. **Configurações do simulador**:

    - Escolha opção `10` para acessar configurações
    - Modifique parâmetros como tema, delay e debug
    - Redefina todas as configurações para os valores padrão
    - Exclua todas as ocorrências

<h2 id="estruturas-de-dados-utilizadas">🎲 Estruturas de Dados Utilizadas</h2>

### 1. **Heap (Fila de Prioridade)**

- **Localização**: `structures/heap_prioridade.py`
- **Uso**: Gerencia ocorrências pendentes ordenadas por severidade e timestamp
- **Complexidade**: O(log n) para inserção e remoção

### 2. **Pilha (Stack)**

- **Localização**: `structures/pilha.py`
- **Uso**: Controla ocorrências em andamento
- **Complexidade**: O(1) para todas as operações

### 3. **Lista Ligada**

- **Localização**: `structures/lista_ligada.py`
- **Uso**: Mantém histórico cronológico de ações
- **Complexidade**: O(1) para inserção no início, O(n) para busca

### 4. **Árvore Binária de Busca**

- **Localização**: `structures/arvore_regioes.py`
- **Uso**: Organiza ocorrências por região geográfica
- **Complexidade**: O(log n) para busca, inserção (caso médio)

<h2 id="configuracoes">⚙️ Configurações</h2>

Você pode modificar as configurações em `config/constants.py`:

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
- [ ] API REST usando Flask/FastAPI
- [ ] Mapas interativos das regiões
- [ ] Métricas de performance das equipes
