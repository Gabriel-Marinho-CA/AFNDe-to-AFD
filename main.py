from AF import AF
from File_Utils import *
from AFNDE_to_AFND import AFNDE_to_AFND
from AFND_to_AFD import AFND_to_AFD
from graphviz import Digraph

def get_line_content(line):
    try:
        return set(line[0:].strip().split(' '))
    except:
        raise ValueError(
            f'Erro ao tentar pegar os valores da linha do arquivo.')

def add_transictions_pattern(Q, A, T):
    try:
        for state in Q:
            for letter in A:
                if T.get(state) is None:
                    T[state] = {}
                T[state][letter] = set()

            T[state]['ê'] = set()
        return T
    except:
        raise ValueError(
            f'Erro ao tentar transformar o set de transicoes em um dicionario.')

def transform_transactions(aux_T, T):
    for transaction in aux_T:
        current_state = transaction[0]
        letter = transaction[1]
        next_state = transaction[2]
        T[current_state][letter].add(next_state)
    return T

if __name__ == "__main__":
    try:
        content_file = open_file('entrada.txt').split('\n')
        content_words = open_file('palavras.txt').split('\n')


        # Definição para afnd-e
        # AF = (A, Q, q, T, F)
        A = {'1', '0'}         # Alfabeto de entrada do autômato
        Q = []          # Estados do autômato
        F = []          # Estados finais do autômato
        T = {}          # Função de transição do autômato
        aux_T = set()   # Auxiliar para construir o mapa de transição
        q = None        # Estado inicial do autômato

        P = []      # Palavras para testar

        line_count = 0

        Q = get_line_content(content_file[0])
        q = content_file[1]
        F = get_line_content(content_file[2])

        content_transition = content_file[3:]

        for line in content_transition:
          transaction = line[0:].strip().split()
          try:
              aux_T.add(
                  (transaction[0], transaction[1], transaction[2]))

          except:
              raise ValueError(
                  f'Não foi possível identificar a transição na linha {line_count}.')

        T = add_transictions_pattern(Q, A, T)
        T = transform_transactions(aux_T, T)

        M_AFNDE = AF(A, Q, q, T, F)
        M_AFND = AFNDE_to_AFND(M_AFNDE)
        M_AFD = AFND_to_AFD(M_AFND)            

        for words in content_words:
          P.append(words)

        for word in P:
          M_AFD.check_word(word)

        # TESTA PALAVRAS
        save_file("saida_palavras.txt", M_AFD.all_checks_str)

        # Salvar a tabela do AFD em um arquivo de saída
        afd_table = "{}\n".format(" ".join(M_AFD.Q))
        afd_table += "{}\n".format(M_AFD.q)
        afd_table += "{}\n".format(" ".join(M_AFD.F))

        for state, transitions in M_AFD.T.items():
            for symbol, next_state in transitions.items():
                afd_table += "{} {} {}\n".format(state, symbol, next_state)

        save_file("afd_tabela.txt", afd_table)

        # Gráfico do AFND
        afnd_graph = Digraph('AFND')
        afnd_graph.attr(rankdir='LR')

        # Defina o estado inicial
        initial_state = q

        # Defina os estados finais
        final_states = F

        # Percorra os estados
        for state, transitions in M_AFNDE.T.items():
            # Adicione um círculo vermelho ao estado inicial
            if state == initial_state:
                afnd_graph.node(state, label=state, shape='circle', color='red')
            # Adicione dois círculos vermelhos aos estados finais
            elif state in final_states:
                afnd_graph.node(state, label=state, shape='doublecircle', color='red')
            else:
                afnd_graph.node(state, label=state)

        # Adicione as transições
        for state, transitions in M_AFNDE.T.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    afnd_graph.edge(state, next_state, label=symbol)

        afnd_graph.render('AFND', format='png')

        # Gráfico do AFD
        afd_graph = Digraph('AFD')
        afd_graph.attr(rankdir='LR')

        final_states_afd = M_AFD.F

        # Percorra os estados
        for state, transitions in M_AFD.T.items():
            # Adicione um círculo vermelho ao estado inicial
            if state == initial_state:
                afd_graph.node(state, label=state, shape='circle', color='red')
            # Adicione dois círculos vermelhos aos estados finais do AFD
            elif state in final_states_afd:
                afd_graph.node(state, label=state, shape='doublecircle', color='red')
            else:
                afd_graph.node(state, label=state)

        # Adicione as transições
        for state, transitions in M_AFD.T.items():
            for symbol, next_state in transitions.items():
                afd_graph.edge(state, next_state, label=symbol)

        afd_graph.render('AFD', format='png')

    except Exception as e:
        print("Ocorreu um erro.")
        print("Exceção: " + str(e))
