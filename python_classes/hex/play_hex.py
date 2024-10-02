from six.moves import input
from hextypes import Player, Point
from hexboard import *
from minimax import *

# Definição de quantidade de colunas para suportar dimensões maiores do tabuleiro
COL_NAMES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 

# Preenchimento do tabuleiro e da posição dos jogadores na primeira e última linha
def print_board(board):
    print('   ' + '   '.join(COL_NAMES[:board.size]))  # Ajuste a impressão para o tamanho do tabuleiro
    for row in range(1, board.size + 1):
        pieces = []
        for col in range(1, board.size + 1):
            piece = board.get(Point(row, col))
            if piece == Player.x:
                pieces.append('X')
            elif piece == Player.o:
                pieces.append('O')
            else:
                pieces.append(' ')
        print('%d  %s' % (row, ' | '.join(pieces)))

# Definição das marcações do mapa de acordo com o tamanho
def point_from_coords(text, size):
    col_name_a = text[0].upper()
    row_a = int(text[1])
    col_name_b = text[2].upper()
    row_b = int(text[3])

    # Verifica se as colunas estão dentro do limite.
    if col_name_a not in COL_NAMES[:size] or col_name_b not in COL_NAMES[:size]:
        raise ValueError("Column name out of bounds.")
    
    return Point(row_a, COL_NAMES.index(col_name_a) + 1), Point(row_b, COL_NAMES.index(col_name_b) + 1)

# Função principal
def main():
    # Solicita ao usuário o tamanho do tabuleiro
    while True:
        try:
            size = int(input("Escolha o tamanho do tabuleiro (por exemplo, 3, 4, 5): "))
            if size < 3:
                print("O tamanho deve ser 3 ou maior.")
                continue
            break
        except ValueError:
            print("Por favor, insira um número válido.")

    game = GameState.new_game(size)  # Inicia o jogo com o tamanho escolhido

    human_player = Player.x
    bot = MinimaxAgent()

    while not game.is_over():
        print_board(game.board)
        if game.next_player == human_player:
            human_move = input('-- ')
            try:
                point_a, point_b = point_from_coords(human_move.strip(), size)
                move = Move(point_a, point_b)
                if not game.is_valid_move(move):
                    print('Movimento inválido.')
                    continue
            except ValueError as e:
                print(e)
                continue
        else:
            move = bot.select_move(game)
            if move is None:
                print('O bot não tem um movimento válido :-(')
                continue
        game = game.apply_move(move)

    print_board(game.board)
    winner = game.winner()
    print('Vencedor: ' + str(winner))

# Execução do programa (while True >> mantém o programa aberto até o cancelamento Ctrl + C)
if __name__ == '__main__':
    while True:
        main()
