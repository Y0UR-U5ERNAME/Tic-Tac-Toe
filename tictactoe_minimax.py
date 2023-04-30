from os import system

grid = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

def dispgrid():
    clear()
    print('   A   B   C\n' + '\n  ───┼───┼───\n'.join([f'{c + 1} ' + '│'.join([f' {j} ' for j in i]) for c, i in enumerate(grid)]))

def playerchoose():
    pos = ""
    while 1:
        dispgrid()
        pos = input(f"\n({turn}) Choose a position (e.g. A1): ").upper()
        if len(pos) == 2 and any(pos.startswith(i) for i in "ABC") and any(pos.endswith(i) for i in "123"):
            if grid[int(pos[1]) - 1][ord(pos[0]) - 65] == " ": break
    grid[int(pos[1]) - 1][ord(pos[0]) - 65] = turn

def cpuchoose():
    poss = []
    if cpu == "X":
        val = float('-inf')
        for a in actions(grid):
            m = minimax(result(grid, a, cpu))
            if m > val:
                val = m
                poss = [a]
            elif m == val:
                poss.append(a)
    elif cpu == "O":
        val = float('inf')
        for a in actions(grid):
            m = minimax(result(grid, a, cpu))
            if m < val:
                val = m
                poss = [a]
            elif m == val:
                poss.append(a)
    
    # debug
    #from time import sleep
    #print(poss)
    #sleep(5)

    # random choice
    from random import choice
    c = choice(poss)
    grid[c[0]][c[1]] = cpu

def minimax(state):
    t = terminal(state)
    if t: return "O X".index(t) - 1

    p = get_player(state)
    if p == "X": # max player
        val = float('-inf')
        for a in actions(state):
            m = minimax(result(state, a, p))
            if m == 1: return 1
            val = max(val, m)
        return val

    if p == "O": # min player
        val = float('inf')
        for a in actions(state):
            m = minimax(result(state, a, p))
            if m == -1: return -1
            val = min(val, m)
        return val

def terminal(state):
    rowscolsdiags = [k for k in [*state, *[[state[j][i] for j in range(3)] for i in range(3)], [m[c] for c, m in enumerate(state)], [n[2-d] for d, n in enumerate(state)]] if len(set(k)) == 1 and ' ' not in k]
    if ["X", "X", "X"] in rowscolsdiags:
        return "X"
    if ["O", "O", "O"] in rowscolsdiags:
        return "O"
    
    if sum(i.count(" ") for i in state) == 0: return " "

def get_player(state):
    return "OX"[sum(i.count(" ") for i in state) % 2]

def actions(state):
    out = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == " ": out.append((i, j))
    return out

def result(state, action, turn):
    g = [[j for j in i] for i in state]
    g[action[0]][action[1]] = turn
    return g

def checkwin():
    if any(all(l == turn for l in k) for k in [*grid, *[[grid[j][i] for j in range(3)] for i in range(3)], [m[c] for c, m in enumerate(grid)], [n[2-d] for d, n in enumerate(grid)]]):
        for c, i in enumerate(grid):
            if all(j == turn for j in i):
                for d, j in enumerate(i):
                    grid[c][d] = f'\x1b[91m{turn}\x1b[0m'
        
        for c, i in enumerate([[grid[j][i] for j in range(3)] for i in range(3)]):
            if all(j == turn for j in i):
                for d, j in enumerate(i):
                    grid[d][c] = f'\x1b[91m{turn}\x1b[0m'
        
        if all(grid[i][i] == turn for i in range(3)):
            for i in range(3):
                grid[i][i] = f'\x1b[91m{turn}\x1b[0m'
        
        if all(grid[i][2-i] == turn for i in range(3)):
            for i in range(3):
                grid[i][2-i] = f'\x1b[91m{turn}\x1b[0m'
                    
        return turn
    if not any([" " in i for i in grid]):
        return " "

def clear(): system("cls||clear")

np = ""
while np not in ["1", "2"]:
    clear()
    np = input("Single or double player? (1 or 2): ")

if np == "1":
    player = ""
    while player not in ["X", "O"]:
        clear()
        player = input("Choose a player (X or O): ").upper()

turn = "X"
if np == "1":
    cpu = "O" if player == "X" else "X"
    if player == "X":
        playerchoose()
    else:
        dispgrid()
        turn = cpu
        cpuchoose()
    while 1:
        if turn == player:
            turn = cpu
            cpuchoose()
            dispgrid()
        else:            
            turn = player
            playerchoose()
        winner = checkwin()
        if winner: break
else:
    while 1:
        playerchoose()
        winner = checkwin()
        if winner: break
        turn = "O" if turn == "X" else "X"

dispgrid()
if winner == " ":
    print("\nIt's a tie!")
else:
    print(f"\n{winner} wins!")