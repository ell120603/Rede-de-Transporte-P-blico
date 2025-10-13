from collections import defaultdict, deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class MetroGraph:
    def __init__(self):
        self.stations = set()
        self.connections = defaultdict(dict)
        self.wait_times = {}

    def _normalize(self, name):
        import unicodedata
        return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII').lower()

    def _find_station(self, name):
        norm = self._normalize(name)
        for s in self.stations:
            if self._normalize(s) == norm:
                return s
        return None

    def add_station(self, name):
        if self._find_station(name) is None:
            self.stations.add(name)

    def remove_station(self, name):
        real_name = self._find_station(name)
        if not real_name:
            return
        self.stations.discard(real_name)
        self.connections.pop(real_name, None)
        for neighbors in self.connections.values():
            neighbors.pop(real_name, None)

    def add_connection(self, from_station, to_station, tempo, linha):
        fs = self._find_station(from_station) or from_station
        ts = self._find_station(to_station) or to_station
        self.stations.update([fs, ts])
        self.connections[fs][ts] = (tempo, linha)
        self.connections[ts][fs] = (tempo, linha)

    def remove_connection(self, from_station, to_station):
        fs = self._find_station(from_station)
        ts = self._find_station(to_station)
        if not fs or not ts:
            return
        self.connections[fs].pop(ts, None)
        self.connections[ts].pop(fs, None)

    def set_wait_time(self, linha, tempo):
        self.wait_times[linha] = tempo

    def get_routes_from(self, station):
        s = self._find_station(station)
        if not s:
            return []
        return list(self.connections[s].items())

    def can_reach(self, start, end):
        s = self._find_station(start)
        e = self._find_station(end)
        if not s or not e:
            return False
        visited = set()
        queue = deque([s])
        while queue:
            current = queue.popleft()
            if current == e:
                return True
            visited.add(current)
            for neighbor in self.connections[current]:
                if neighbor not in visited:
                    queue.append(neighbor)
        return False

    def shortest_path(self, start, end):
        s = self._find_station(start)
        e = self._find_station(end)
        if not s or not e:
            return None, float('inf'), 0

        heap = [(0, s, [], None, 0)] 
        visited = {}

        while heap:
            tempo_total, current, path, linha_ant, trocas = heapq.heappop(heap)
            if current == e:
                return path + [current], tempo_total, trocas

            if current in visited and visited[current] <= tempo_total:
                continue
            visited[current] = tempo_total

            for neighbor, (tempo, linha) in self.connections[current].items():
                wait = 0
                trocas_novas = trocas
                if linha_ant and linha_ant != linha:
                    wait = self.wait_times.get(linha, 0)
                    trocas_novas += 1
                heapq.heappush(
                    heap,
                    (tempo_total + tempo + wait, neighbor, path + [current], linha, trocas_novas)
                )

        return None, float('inf'), 0

    def all_paths(self, start, end, max_depth=10):
        s = self._find_station(start)
        e = self._find_station(end)
        if not s or not e:
            return []

        def dfs(atual, destino, visitados, caminho, total_tempo):
            if len(caminho) > max_depth:
                return []
            if atual == destino:
                return [(caminho[:], total_tempo)]
            resultados = []
            for vizinho, (tempo, linha) in self.connections[atual].items():
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    resultados.extend(
                        dfs(vizinho, destino, visitados, caminho + [vizinho], total_tempo + tempo)
                    )
                    visitados.remove(vizinho)
            return resultados

        return dfs(s, e, {s}, [s], 0)

    def plot_graph(self):
        G = nx.Graph()
        for est1, vizinhos in self.connections.items():
            for est2, (tempo, linha) in vizinhos.items():
                G.add_edge(est1, est2, weight=tempo, line=linha)

        
        cores_linhas = {
            'Azul': '#0070BB',
            'Verde': '#009739',
            'Vermelha': '#ED1C24',
            'Amarela': '#FFD700',
            'Lilás': '#A757A8',
            'Prata': '#C0C0C0',
            'Turquesa': '#40E0D0',
            'Laranja': '#FF6F00',
            'Rubi': '#A91101',
            'Esmeralda': '#009B77',
            'Safira': '#082567'
        }

        pos = nx.kamada_kawai_layout(G)

        plt.figure(figsize=(10, 8))
        plt.title("🗺️  Mapa do Metrô de SP", fontsize=14, fontweight='bold', pad=20)

        
        for linha, cor in cores_linhas.items():
            edges = [(u, v) for u, v, d in G.edges(data=True) if d['line'] == linha]
            if edges:
                nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color=cor, label=linha)

        
        nx.draw_networkx_nodes(G, pos, node_color='white', edgecolors='black', node_size=900)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, label_pos=0.5)

        
        plt.legend(title="Linhas do Metrô", loc="upper left", bbox_to_anchor=(1, 1))
        plt.axis('off')
        plt.tight_layout()
        plt.show()
