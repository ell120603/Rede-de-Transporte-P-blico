

```markdown
# 🚉 4. Rede de Transporte Público (Ônibus/Metrô) - Sistema de Metrô SP

## 📌 Descrição do Projeto

Este projeto consiste na modelagem de uma rede de transporte público (especificamente, o Metrô de São Paulo) utilizando a teoria de grafos.

As **Estações** são representadas como **Vértices** (Nós) do grafo, e as **Conexões** entre as estações (os trechos de linha) são as **Arestas**. O **Peso** de cada aresta é o tempo de viagem (em minutos) entre as estações.

A solução implementa o famoso algoritmo de **Dijkstra** para encontrar o trajeto mais rápido entre duas estações, considerando o tempo de viagem e o tempo de espera para baldeações (troca de linhas).

## 💡 Tecnologias Utilizadas

* **Python 3.x**
* **`networkx`:** Para manipulação e análise de grafos.
* **`matplotlib`:** Para a visualização do grafo (mapa do metrô).
* **`heapq` e `collections`:** Para a implementação eficiente de algoritmos de grafo (Dijkstra e BFS).

## 📂 Estrutura do Projeto

```

.
├── main.py                   \# Lógica principal, menu de interação e inicialização do grafo.
├── src/
│   ├── metro_graph.py        \# Classe central `MetroGraph` (a lógica do grafo).
│   └── sp_metro_data.py      \# Dados iniciais das linhas e tempos de espera do metrô de SP.
└── README.md

````

## ✨ Funcionalidades

O projeto atende aos requisitos básicos de modelagem de grafos e inclui funcionalidades extras para simular uma rede de transporte real.

### 🎯 Requisitos Principais

| Funcionalidade | Implementação no Código |
| :--- | :--- |
| **Adicionar/remover estações (vértices)** | Métodos `add_station()` e `remove_station()` |
| **Adicionar/remover conexões (arestas com tempo)** | Métodos `add_connection()` e `remove_connection()` |
| **Consultar rotas disponíveis de uma estação** | Método `get_routes_from()` |
| **Verificar se é possível chegar de uma estação a outra** | Método `can_reach()` (utiliza Busca em Largura - BFS) |
| **Calcular o trajeto mais rápido (Dijkstra)** | Método `shortest_path()` (implementação do Algoritmo de Dijkstra) |
| **Plotar o Grafo** | Método `plot_graph()` (utiliza `networkx` e `matplotlib` para visualização) |

### ⭐ Extras Implementados

| Funcionalidade Extra | Implementação no Código |
| :--- | :--- |
| **Adicionar tempo de espera entre linhas** | O método `set_wait_time()` permite definir o tempo de espera. O algoritmo de Dijkstra (`shortest_path()`) considera este tempo como um custo adicional ao trocar de linha (baldeação). |
| **Calcular o melhor trajeto com baldeações** | O `shortest_path()` otimizado com Dijkstra encontra o trajeto mais rápido, minimizando o tempo total (tempo de viagem + tempo de espera de baldeação). |
| **Todas as rotas possíveis** | Método `all_paths()` (utiliza Busca em Profundidade - DFS para listar caminhos). |

## 🚀 Como Executar

Siga os passos abaixo para configurar e rodar o projeto em sua máquina.

### Pré-requisitos

Certifique-se de ter o Python instalado. As dependências podem ser instaladas com `pip`:

```bash
pip install networkx matplotlib
````

### Inicialização

1.  Clone o repositório ou baixe os arquivos.
2.  Navegue até o diretório principal do projeto.
3.  Execute o arquivo principal:

<!-- end list -->

```bash
python main.py
```

## 🖥️ Uso do Sistema

Ao executar o `main.py`, um menu interativo será exibido no terminal, permitindo que você gerencie o grafo do metrô e realize consultas.

```
bem-vindo ao sistema de metrô!

--- METRÔ SP ---
1. Adicionar estação
2. Remover estação
3. Adicionar conexão
4. Remover conexão
5. Consultar rotas de uma estação
6. Verificar se é possível chegar de uma estação a outra
7. Calcular trajeto mais rápido (Dijkstra)
8. Adicionar tempo de espera entre linhas
9. Mostrar todas as estações
10. Todas as rotas possíveis
11. Plotar grafo do metrô
12. Sair
Escolha uma opção:
```

### Exemplo de Uso (Trajeto Mais Rápido)

Ao selecionar a opção `7`, você pode calcular o trajeto mais eficiente:

**Entrada:**

```
7
Origem: Se
Destino: Luz
```

**Saída Esperada:**

```
Melhor trajeto: Se -> São Bento -> Luz
Tempo total: X min
Baldeações: Y
```

*(Os valores de tempo e baldeações dependerão da configuração atual em `sp_metro_data.py`)*

### Observação sobre persistência

As opções de adicionar/remover estações, conexões e tempos de espera (opções 1, 3 e 8) utilizam a função `salvar_dados()` para tentar persistir as alterações diretamente no arquivo `src/sp_metro_data.py`.

```
```
