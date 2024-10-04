#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 8  // Número de rainhas e tamanho do tabuleiro
#define MAX_STEPS 1000  // Número máximo de passos para tentar encontrar uma solucao

int move_count = 0;

// Função para ler o tabuleiro do usuário
void read_user_board(int board[N]) {
    char line[N + 1];
    for (int i = 0; i < N; i++) {
        printf("Digite a linha %d de %d (use '.' para espaco vazio e 'R' para rainha): ", i + 1, N);
        scanf("%s", line);

        for (int j = 0; j < N; j++) {
            if (line[j] == 'R') {
                board[j] = i;
            }
        }
    }
}

// Função para gerar uma configuração aleatória inicial
void generate_random_board(int board[N]) {
    for (int i = 0; i < N; i++) {
        board[i] = rand() % N;
    }
}

// Função para contar o número de conflitos para uma rainha em uma posição específica
int calculate_conflicts(int board[N], int row, int col) {
    int conflicts = 0;
    for (int i = 0; i < N; i++) {
        if (i == col) continue;
        int other_row = board[i];

        // Verifica se há conflito de linha ou diagonal
        if (other_row == row || abs(other_row - row) == abs(i - col)) {
            conflicts++;
        }
    }
    return conflicts;
}

// Função para encontrar a melhor linha para uma rainha em uma determinada coluna
int find_min_conflict_row(int board[N], int col) {
    int min_conflicts = N;
    int best_row = board[col];

    for (int row = 0; row < N; row++) {
        int conflicts = calculate_conflicts(board, row, col);
        if (conflicts < min_conflicts) {
            min_conflicts = conflicts;
            best_row = row;
        }
    }

    return best_row;
}

// Função para resolver o problema das N rainhas usando Min-Conflicts
int solve_n_queens_min_conflicts(int board[N]) {
    for (int step = 0; step < MAX_STEPS; step++) {
        // Verificar se o tabuleiro está sem conflitos
        int total_conflicts = 0;

        for (int col = 0; col < N; col++) {
            total_conflicts += calculate_conflicts(board, board[col], col);
        }

        if (total_conflicts == 0) {
            return 1;  // Solucao encontrada
        }

        // Escolher uma coluna aleatória com conflito
        int col = rand() % N;
        int conflicts = calculate_conflicts(board, board[col], col);
        while (conflicts == 0) {
            col = rand() % N;
            conflicts = calculate_conflicts(board, board[col], col);
        }

        // Encontrar a melhor linha para a rainha nessa coluna
        int best_row = find_min_conflict_row(board, col);

        // Mover a rainha para a posição com menos conflitos
        if (board[col] != best_row) {
            board[col] = best_row;
            move_count++;
        }
    }

    return 0;  // Não foi possível encontrar uma solucao
}

// Função para imprimir o tabuleiro
void print_board(int board[N]) {
    for (int row = 0; row < N; row++) {
        for (int col = 0; col < N; col++) {
            if (board[col] == row) {
                printf("R ");
            } else {
                printf(". ");
            }
        }
        printf("\n");
    }
    printf("\n");
}

int main() {
    srand(time(0));
    int board[N];
    int escolha;

    printf("Escolha o modo de entrada do tabuleiro:\n");
    printf("1. Gerar um tabuleiro aleatorio\n");
    printf("2. Montar o tabuleiro manualmente\n");
    scanf("%d", &escolha);

    if (escolha == 1) {
        generate_random_board(board);
    } else if (escolha == 2) {
        read_user_board(board);
    } else {
        printf("Escolha invalida.\n");
        return 1;
    }

    // Resolver o problema das N rainhas
    if (solve_n_queens_min_conflicts(board)) {
        printf("Numero de mudancas realizadas: %d\n", move_count);
        print_board(board);   
    } else {
        printf("Nao foi possivel encontrar uma solucao dentro do limite de passos.\n");
    }


    return 0;
}
