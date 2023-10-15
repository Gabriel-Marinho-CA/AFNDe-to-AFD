from AF import AF
from copy import deepcopy


def is_this_state_have_just_empty_transactions(state, AF: AF):
    just_empty_transactions = True
    transactions = AF.T[state]
    for symbol, next_states in transactions.items():
        if symbol != 'ê' and len(next_states) > 0:
            just_empty_transactions = False
    return just_empty_transactions

# elimina todas transicoes vazias do automado nao deterministico


def AFNDE_to_AFND(AFNDE: AF):
    try:
        AFND = deepcopy(AFNDE)
        transactions = AFND.T

        # A principal ideia eh usar ê+ - fechamento (estado)
        # ê+(q) = todos os estados alcancaveis por ê a partir de um estado 'q'
        #  logo a nova funcao de transicao sera T(q, a) = T(q, a) + ê+(q)
        # isto eh, na transicao vazia tera uma transicao com todas letras do alfabeto
        # depois 'ignorar' estados que tenham apenas transicoes vazias
        all_e_plus = {}

        # Nos casos de ter um estado que soh possui transicoes vazias sera feito uma ligacao direta com o primeiro estado
        # que nao tiver apenas transicoes vazias
        merge_states = []

        states_to_ignore = set()

        # percorro pelos estados e nao pelo estado inicial e ir descobrindo
        # pq pensei no caso de uma funcao de transicao representado num grafo bipartido
        # se em ambos tiverem transicoes vazias ele nao vai retornar uma afnd (que nao deve ter esse tipo de transicao)
        for state in AFND.Q:
            # vai guardar todos estados ligados diretamente a esse por transicao vazia
            e_plus = set()

            # uma pilha que vai ajudar a achar todos estados com ligacao por transicao vazia
            states_queue = deepcopy(transactions[state]['ê'])

            # checa se o estado atual tem apenas transicoes vazias para poder ignorar ele
            if (is_this_state_have_just_empty_transactions(state, AFNDE)):
                states_to_ignore.add(state)
                for next_state in transactions[state]['ê']:
                    merge_st = tuple((state, next_state))
                    merge_states.append(merge_st)

            # busca pelos estados ligados por transicao vazia
            while (len(states_queue) > 0):
                cur_state = states_queue.pop()
                e_plus.add(cur_state)

                for new_state in transactions[cur_state]['ê']:
                    if new_state not in e_plus and new_state not in states_queue:
                        states_queue.add(new_state)
            all_e_plus[state] = e_plus

        for state in states_to_ignore:
            AFND.Q.remove(state)
            AFND.T.pop(state, None)

        # troca as transicoes para um estado que soh tem transicao vazia para o proximo (ignora o estado)
        # alem de apagar todas transicoes vazias dos estados
        # TODO: tomar cuidado quando for estado final ou inicial (talvez nao fazer nesses casos)
        for state in AFND.Q:
            transactions[state].pop('ê')
            for symbol in transactions[state]:
                aux = list(transactions[state][symbol])
                aux2 = list(all_e_plus[state])
                transactions[state][symbol] = set(aux + aux2)

                states_of_symbol = transactions[state][symbol]
                for states_tuple in merge_states:
                    if states_tuple[0] in states_of_symbol:
                        states_of_symbol.discard(states_tuple[0])
                        states_of_symbol.add(states_tuple[1])

        return AFND
    except:
        raise ValueError(f'Erro ao tentar transformar AFNDE em AFND.')
