import enum
import random

from base import Agent

__all__ = [
    'MinimaxAgent',
]


# tag::gameresult-enum[]
class GameResult(enum.Enum):
    loss = 1
    win = 2
# end::gameresult-enum[]


def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    else:
        return game_result.loss


# tag::minimax-signature[]
def best_result(game_state, depth):
# end::minimax-signature[]
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        else:
            return GameResult.loss

    # Limitar a profundidade da busca na resposta do agente
    if depth == 0:
        return GameResult.loss  # Ou uma avaliação padrão

# tag::minimax-recursive-case[]
    best_result_so_far = GameResult.loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)     # <1> # Visibilidade sobre o tabuleiro para cada movimento feito
        opponent_best_result = best_result(next_state, depth - 1)  # <2> Encontra o melhor movimento do oponente com o limitador aplicado
        our_result = reverse_game_result(opponent_best_result) # <3> Pensamento oposto ao do oponente
        if our_result.value > best_result_so_far.value:        # <4> Comparação do resultado com o melhor visto até o momento
            best_result_so_far = our_result
    return best_result_so_far
# end::minimax-recursive-case[]

# tag::minimax-agent[]

class MinimaxAgent:
    def __init__(self, max_depth=3): # Definição do limite de profundidade do agente para responder mais rápido (pensa menos)
        self.max_depth = max_depth

    def select_move(self, game_state):
        winning_moves = []
        losing_moves = []

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(next_state, self.max_depth)  # Passa a profundidade na leitura do oponente
            our_best_outcome = reverse_game_result(opponent_best_outcome)

            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)

        if winning_moves:
            return random.choice(winning_moves)
        if losing_moves:
            return random.choice(losing_moves)
        return None
# end::minimax-agent[]