from AF import AF
from AFD import AFD
from copy import deepcopy

# Mesclas estrutura


def merge_dict(a: dict, b: dict):
    keys = list(b.keys())
    new_dict = deepcopy(a)

    for key in keys:
        if key in a.keys():
            new_dict[key] = new_dict[key].union(b[key])
        else:
            new_dict[key] = b[key]

    return new_dict

# Mesclas estados (q0q1, q0q1q2, etc...)


def merge_states(states):
    aux = list("".join(states))
    aux = list(dict.fromkeys(aux))
    aux.sort()

    return "".join(aux)

# Mesclas as transições


def merge_transition(states, in_state, afnd: AF):
    transition = {}
    for state in states:
        transition = merge_dict(transition, afnd.T[state])

    afnd.T[in_state] = transition

# Verifica possui transição não deterministica


def has_transitions_non_deterministic(afnd: AF):
    for transitions in afnd.T.values():
        for transition in transitions:
            if len(transitions[transition]) > 1:
                return True
    return False

# Verifica se é estadp final


def is_final_state(afnd: AF, transition):
    for state in afnd.F:
        if state in transition:
            return True
    return False

# elimina todas transicoes ambiguas transformando em um automato deterministico


def AFND_to_AFD(afnde: AF):
    try:
        afnd = deepcopy(afnde)

        # Converte o AFNDE para AFND
        while has_transitions_non_deterministic(afnd):
            afnd_aux = deepcopy(afnd)
            for state, transitions in afnd.T.items():
                for transition in transitions:
                    if len(transitions[transition]) > 1:
                        new_state = merge_states(transitions[transition])
                        if new_state not in afnd_aux.Q:
                            afnd_aux.Q.add(new_state)
                            afnd_aux.T[new_state] = set()

                            merge_transition(
                                transitions[transition], new_state, afnd_aux)
                            if is_final_state(afnde, transitions[transition]):
                                afnd_aux.F.add(new_state)

                        afnd_aux.T[state][transition] = {new_state}

            afnd = afnd_aux

        # Busca estados visitados
        visited_state = []
        state_to_visit = [afnd.q]
        while state_to_visit:
            cur_state = state_to_visit.pop()
            if cur_state not in visited_state:
                visited_state.append(cur_state)

            for transition in afnd.T[cur_state].values():
                if list(transition)[0] not in visited_state + state_to_visit:
                    state_to_visit.append(list(transition)[0])

        # Retira os estados não visitados
        for state in afnd.Q.copy():
            if state not in visited_state:
                afnd.Q.discard(state)
                afnd.F.discard(state)
                del afnd.T[state]

        # Deixa transicoes com valor unico, se tornando assim um automato deterministico
        for state in afnd.Q:
            transactions = afnd.T[state]
            for symbol in transactions.keys():
                transactions[symbol] = list(transactions[symbol])[0]

        afd = AFD(afnd.A, afnd.Q, afnd.q, afnd.T, afnd.F)
        return afd
    except:
        raise ValueError(f'Erro ao tentar transformar AFND em AFD.')