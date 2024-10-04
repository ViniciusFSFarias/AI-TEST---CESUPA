import random
import time

N = 8  # Número de rainhas e tamanho do tabuleiro
MAX_STEPS = 1000  # Número máximo de passos para tentar encontrar uma solução

move_count = 0

# Função para ler o tabuleiro do usuário
def read_user_board():
    board = [-1] * N
    for i in range(N):
        line = input(f"Digite a linha {i + 1} de {N} (use '.' para espaço vazio e 'R' para rainha): ")

        for j in range(N):
            if line[j] == 'R':
                board[j] = i
    return board

# Função para gerar uma configuração aleatória inicial
def generate_random_board():
    return [random.randint(0, N - 1) for _ in range(N)]

# Função para contar o número de conflitos para uma rainha em uma posição específica
def calculate_conflicts(board, row, col):
    conflicts = 0
    for i in range(N):
        if i == col:
            continue
        other_row = board[i]
        
        # Verifica se há conflito de linha ou diagonal
        if other_row == row or abs(other_row - row) == abs(i - col):
            conflicts += 1
    return conflicts

# Função para encontrar a melhor linha para uma rainha em uma determinada coluna
def find_min_conflict_row(board, col):
    min_conflicts = N
    best_row = board[col]  # Padrão: posição atual

    for row in range(N):
        conflicts = calculate_conflicts(board, row, col)
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_row = row

    return best_row

# Função para resolver o problema das N rainhas usando Min-Conflicts
def solve_n_queens_min_conflicts(board):
    global move_count
    for step in range(MAX_STEPS):
        # Verificar se o tabuleiro está sem conflitos
        total_conflicts = sum(calculate_conflicts(board, board[col], col) for col in range(N))

        if total_conflicts == 0:
            return True  # Solução encontrada

        # Escolher uma coluna aleatória com conflito
        col = random.randint(0, N - 1)
        conflicts = calculate_conflicts(board, board[col], col)
        while conflicts == 0:
            col = random.randint(0, N - 1)
            conflicts = calculate_conflicts(board, board[col], col)

        # Encontrar a melhor linha para a rainha nessa coluna
        best_row = find_min_conflict_row(board, col)

        # Mover a rainha para a posição com menos conflitos
        if board[col] != best_row:
            board[col] = best_row
            move_count += 1

    return False  # Não foi possível encontrar uma solução

# Função para imprimir o tabuleiro
def print_board(board):
    for row in range(N):
        for col in range(N):
            if board[col] == row:
                print("R", end=" ")
            else:
                print(".", end=" ")
        print()
    print()

# Função principal
def main():
    global move_count
    random.seed(time.time())  # Semente para números aleatórios

    escolha = int(input("Escolha o modo de entrada do tabuleiro:\n1. Gerar um tabuleiro aleatório\n2. Montar o tabuleiro manualmente\n"))

    if escolha == 1:
        board = generate_random_board()
    elif escolha == 2:
        board = read_user_board()
    else:
        print("Escolha inválida.")
        return

    # Resolver o problema das N rainhas
    if solve_n_queens_min_conflicts(board):
        print(f"Tabuleiro original:\n\n")
        print_board(board)
        print(f"Número de mudanças realizadas: {move_count}")
        print_board(board)
    else:
        print(f"Tabuleiro original:\n\n")
        print_board(board)
        print("Não foi possível encontrar uma solução dentro do limite de passos.")

if __name__ == "__main__":
    main()
