from pyamaze import maze,agent,COLOR,textLabel
from queue import PriorityQueue
from collections import deque


#region funções do menu
def menu():
    print("""
      SIMULADOR DE BUSCA A-ESTRELA
    """)

def obter_dimensoes_labirinto():
    altura = int(input("Digite a altura do labirinto (quantas linhas): "))
    largura = int(input("Digite a largura do labirinto (quantas colunas): "))
    return altura, largura

def obter_fator_randomizacao():
    fator = int(input("Digite o fator de randomização para o labirinto (0 = labirinto de solução única, valores maiores oferecem mais caminhos e mais loops): "))
    return fator

def obter_posicao_agente(tipo, max_linhas, max_colunas):
    linha = int(input(f"Digite a linha de {tipo} do agente (1 - {max_linhas}): "))
    coluna = int(input(f"Digite a coluna de {tipo} do agente (1 - {max_colunas}): "))
    return linha, coluna
#endregion

#region busca a-estrela
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))
    
def aStar(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    open = PriorityQueue()
    open.put((h(start, m._goal), h(start, m._goal), start))
    aPath = {}
    g_score = {row: float("inf") for row in m.grid}
    g_score[start] = 0
    f_score = {row: float("inf") for row in m.grid}
    f_score[start] = h(start, m._goal)
    searchPath=[start]
    while not open.empty():
        currCell = open.get()[2]
        searchPath.append(currCell)
        if currCell == m._goal:
            break        
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, m._goal)

                if temp_f_score < f_score[childCell]:   
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_g_score + h(childCell, m._goal)
                    open.put((f_score[childCell], h(childCell, m._goal), childCell))


    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath
#endregion

if __name__ == '__main__':
    menu()

    altura, largura = obter_dimensoes_labirinto()
    fator_randomizacao = obter_fator_randomizacao()

    origem = obter_posicao_agente("origem", altura, largura)
    destino = obter_posicao_agente("destino", altura, largura)

    print("\nConfigurações selecionadas:")
    print(f"Tamanho do labirinto: {altura}x{largura}")
    print(f"Fator de randomização: {fator_randomizacao}")
    print(f"Posição de origem: {origem}")
    print(f"Posição de destino: {destino}")

    
    m=maze(altura,largura)
    m.CreateMaze(destino[0],destino[1],loopPercent=fator_randomizacao)

    searchPath,aPath,fwdPath=aStar(m,(origem[0],origem[1]))

    a=agent(m,origem[0],origem[1],footprints=True,color=COLOR.blue,filled=True)
    b=agent(m,destino[0],destino[1],footprints=True,color=COLOR.yellow,filled=True,goal=(origem[0],origem[1]))
    c=agent(m,origem[0],origem[1],footprints=True,color=COLOR.red,goal=(destino[0],destino[1]))
        
    m.tracePath({a:searchPath},delay=200)
    m.tracePath({b:aPath},delay=200)
    m.tracePath({c:fwdPath},delay=200)

    l=textLabel(m,'A Star Path Length',len(fwdPath)+1)
    l=textLabel(m,'A Star Search Length',len(searchPath))

    m.run()
    