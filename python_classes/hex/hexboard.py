import copy

from hextypes import Player, Point
from play_hex import *

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass

# Montagem do tabuleiro (padrão 3x3)
BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))
# Diagonal principal (Canto Superior Esquerdo --- Canto Inferior Direito)
DIAG_1 = (Point(1, 1), Point(2, 2), Point(3, 3))
# Diagonal inversa (Canto Superior Direito --- Canto Inferior Esquerdo)
DIAG_2 = (Point(1, 3), Point(2, 2), Point(3, 1))

# Definição do tabuleiro
class Board:
    
    def __init__(self, size):
        self.size = size  # Armazena o tamanho do tabuleiro
        self._grid = {}
        # Preenche as linhas inicial e final com os jogadores
        for col in range(1, size + 1):
            self._grid[Point(1, col)] = Player.o  # Jogador O na linha superior
            self._grid[Point(size, col)] = Player.x  # Jogador X na linha inferior

    def is_on_grid(self, point):
        return 1 <= point.row <= self.size and 1 <= point.col <= self.size

    def get(self, point):
        """Retorna o conteúdo de um ponto no tabuleiro.
        Retorna None se o ponto estiver vazio, ou um Player se houver uma peça nesse ponto.
        """
        return self._grid.get(point)

    def place(self, player, point_a, point_b):
        assert self.is_on_grid(point_a)
        assert self.is_on_grid(point_b)
        self._grid[point_a] = None  # Remove a peça do ponto A
        self._grid[point_b] = player  # Coloca a peça do jogador no ponto B

# Definição do movimento
class Move:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

# Definição do Estado do Jogo (Regras implementadas para o funcionamento do jogo)
class GameState:
    
    def __init__(self, size):
        self.size = size
        self.board = self.create_board()
        self.next_player = Player.x  # Jogador que começa
        self.winner = None

    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    @classmethod
    def new_game(cls, size):
        board = Board(size)  # Passa o tamanho do tabuleiro
        return GameState(board, Player.x, None)

    def is_valid_move(self, move):
    # Adiciona a verificação do tamanho do tabuleiro
        if not self.board.is_on_grid(move.point_a) or not self.board.is_on_grid(move.point_b):
            return False

        # pontos A e B devem ser diferentes
        if move.point_a == move.point_b:
            return False

        # o jogo deve ainda estar em andamento
        if self.is_over():
            return False

        # ponto A deve pertencer ao próximo jogador
        if self.next_player != self.board.get(move.point_a):
            return False

        # Se B está na mesma coluna, deve ser um movimento simples para a próxima linha
        if move.point_a.col == move.point_b.col:
            if self.board.get(move.point_b) is None and abs(move.point_a.row - move.point_b.row) == 1:
                return True

        # Verifica se A e B pertencem a jogadores diferentes
        if self.board.get(move.point_b) is not None and \
        self.board.get(move.point_a) != self.board.get(move.point_b) and \
        move.point_a.col != move.point_b.col and move.point_a.row != move.point_b.row and \
        abs(move.point_a.col - move.point_b.col) == 1 and abs(move.point_a.row - move.point_b.row) == 1:
            return True

        return False

    # Definição de quem cruzou o outro lado do tabuleiro
    def _has_crossed_board(self, player):
        if player == Player.x:
            for col in range(1, self.board.size + 1):
                if self.board.get(Point(1, col)) == Player.x:
                    return True
        else:  # Player.o
            for col in range(1, self.board.size + 1):
                if self.board.get(Point(self.board.size, col)) == Player.o:
                    return True
        return False

    def apply_move(self, move):
        """Retorna o novo GameState após aplicar o movimento."""
        next_board = copy.deepcopy(self.board)
        if move is not None:
            next_board.place(self.next_player, move.point_a, move.point_b)
        return GameState(next_board, self.next_player.other, move)

    def legal_moves(self):
        moves = []
        for row in range(1, self.board.size + 1):
            for col in range(1, self.board.size + 1):
                if self.board.get(Point(row, col)) == Player.o:  # Jogador O
                    # Tentar movimentos para a próxima linha
                    for delta_col in [-1, 0, 1]:  # Colunas adjacentes
                        next_row = row + 1
                        next_col = col + delta_col
                        if self.board.is_on_grid(Point(next_row, next_col)):
                            move = Move(Point(row, col), Point(next_row, next_col))
                            if self.is_valid_move(move):
                                moves.append(move)
                elif self.board.get(Point(row, col)) == Player.x:  # Jogador X
                    # Tentar movimentos para a linha anterior
                    for delta_col in [-1, 0, 1]:  # Colunas adjacentes
                        next_row = row - 1
                        next_col = col + delta_col
                        if self.board.is_on_grid(Point(next_row, next_col)):
                            move = Move(Point(row, col), Point(next_row, next_col))
                            if self.is_valid_move(move):
                                moves.append(move)

        return moves

    def is_over(self):
        # A lógica de vitória e condições de fim de jogo pode permanecer, sujeito a adaptações
        if self._has_crossed_board(Player.x):
            return True
        if self._has_crossed_board(Player.o):
            return True
        
        for row in range(1, self.board.size + 1):
            for col in range(1, self.board.size + 1):
                if self.next_player == Player.o and self.board.get(Point(row, col)) == Player.o:
                    # Lógica para verificar se o jogador O pode se mover
                    if self.board.get(Point(row + 1, col)) is None or \
                       self.board.get(Point(row + 1, col + 1)) == Player.x or \
                       self.board.get(Point(row + 1, col - 1)) == Player.x:
                        return False
                if self.next_player == Player.x and self.board.get(Point(row, col)) == Player.x:
                    # Lógica para verificar se o jogador X pode se mover
                    if self.board.get(Point(row - 1, col)) is None or \
                       self.board.get(Point(row - 1, col + 1)) == Player.o or \
                       self.board.get(Point(row - 1, col - 1)) == Player.o:
                        return False
        return True

    def winner(self):
        if self._has_crossed_board(Player.x):
            return Player.x
        elif self._has_crossed_board(Player.o):
            return Player.o
        elif self.next_player == Player.x:
            return Player.o
        else:
            return Player.x
