from src.metro_graph import MetroGraph
from src.sp_metro_data import sp_metro_lines, sp_wait_times

import sys
import os

def inicializa_metro():
    metro = MetroGraph()
    for linha, conexoes in sp_metro_lines.items():
        for est1, est2, tempo in conexoes:
            metro.add_connection(est1, est2, tempo, linha)
    for linha, tempo in sp_wait_times.items():
        metro.set_wait_time(linha, tempo)
    return metro

def salvar_dados(estacao=None, conexao=None, linha=None, tempo_espera=None):
    file_path = os.path.join(os.path.dirname(__file__), 'src', 'sp_metro_data.py')
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    local_vars = {}
    exec(code, {}, local_vars)
    sp_metro_lines = local_vars['sp_metro_lines']
    sp_wait_times = local_vars['sp_wait_times']

    if estacao and linha:
        if linha not in sp_metro_lines:
            sp_metro_lines[linha] = []

    if conexao and linha:
        if linha not in sp_metro_lines:
            sp_metro_lines[linha] = []
        if conexao not in sp_metro_lines[linha]:
            sp_metro_lines[linha].append(conexao)

    if tempo_espera and linha:
        sp_wait_times[linha] = tempo_espera

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('sp_metro_lines = ' + repr(sp_metro_lines) + '\n\n')
        f.write('sp_wait_times = ' + repr(sp_wait_times) + '\n')

def menu():
    metro = inicializa_metro()
    while True:
        print("\nbem-vindo ao sistema de metrô!")
        print("\n--- METRÔ SP ---")
        print("1. Adicionar estação")
        print("2. Remover estação")
        print("3. Adicionar conexão")
        print("4. Remover conexão")
        print("5. Consultar rotas de uma estação")
        print("6. Verificar se é possível chegar de uma estação a outra")
        print("7. Calcular trajeto mais rápido (Dijkstra)")
        print("8. Adicionar tempo de espera entre linhas")
        print("9. Mostrar todas as estações")
        print("10. Todas as rotas possíveis")
        print("11. Plotar grafo do metrô")
        print("12. Sair")
        op = input("Escolha uma opção: ")
        if op == '1':
            nome = input("Nome da estação: ")
            linha = input("Linha da estação: ")
            metro.add_station(nome)
            salvar_dados(estacao=nome, linha=linha)
            print(f"Estação '{nome}' adicionada.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '2':
            nome = input("Nome da estação: ")
            metro.remove_station(nome)
            print(f"Estação '{nome}' removida.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '3':
            est1 = input("Estação de origem: ")
            est2 = input("Estação de destino: ")
            tempo = int(input("Tempo entre elas (min): "))
            linha = input("Linha: ")
            metro.add_connection(est1, est2, tempo, linha)
            salvar_dados(conexao=(est1, est2, tempo), linha=linha)
            print(f"Conexão adicionada entre '{est1}' e '{est2}' pela linha '{linha}'.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '4':
            est1 = input("Estação de origem: ")
            est2 = input("Estação de destino: ")
            metro.remove_connection(est1, est2)
            print(f"Conexão removida entre '{est1}' e '{est2}'.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '5':
            est = input("Estação: ")
            rotas = metro.get_routes_from(est)
            if not rotas:
                print("Nenhuma rota encontrada.")
            else:
                for dest, (tempo, linha) in rotas:
                    print(f"-> {dest} | Tempo: {tempo} min | Linha: {linha}")
            input("Digite 0 para voltar ao menu: ")
        elif op == '6':
            est1 = input("Origem: ")
            est2 = input("Destino: ")
            if metro.can_reach(est1, est2):
                print(f"É possível chegar de '{est1}' a '{est2}'.")
            else:
                print(f"Não é possível chegar de '{est1}' a '{est2}'.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '7':
            est1 = input("Origem: ")
            est2 = input("Destino: ")
            caminho, tempo, trocas = metro.shortest_path(est1, est2)
            if caminho:
                 print(f"\nMelhor trajeto: {' -> '.join(caminho)}")
                 print(f" Tempo total: {tempo} min")
                 print(f" Baldeações: {trocas}")
            else:
                print("Não há trajeto disponível.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '8':
            linha = input("Linha: ")
            tempo = int(input("Tempo de espera (min): "))
            metro.set_wait_time(linha, tempo)
            salvar_dados(linha=linha, tempo_espera=tempo)
            print(f"Tempo de espera da linha '{linha}' atualizado para {tempo} min.")
            input("Digite 0 para voltar ao menu: ")
        elif op == '9':
            estacoes = metro.show_stations()
            print("\nEstações cadastradas:")
            for est in estacoes:
                print(f"- {est}")
            input("Digite 0 para voltar ao menu: ")
        elif op == '10':
            est1 = input("Origem: ")
            est2 = input("Destino: ")
            rotas = metro.all_paths(est1, est2)
            if not rotas:
                print("Nenhuma rota encontrada.")
            else:
                 print(f"\nForam encontradas {len(rotas)} rotas possíveis:\n")
                 for i, (path, tempo) in enumerate(rotas, 1):
                     print(f"{i}. {' -> '.join(path)} | Tempo: {tempo} min")
            input("Digite 0 para voltar ao menu: ")
        elif op == '11':
            metro.plot_graph()
            print("Gerando visualização do grafo...")
            input("Digite 0 para voltar ao menu: ")
        elif op == '12':
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida.")
            input("Digite 0 para voltar ao menu: ")

if __name__ == "__main__":
    menu()

