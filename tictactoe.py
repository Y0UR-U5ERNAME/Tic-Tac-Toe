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
    weights = [[0 if j == " " else -1 for j in i] for i in grid]

    #rows
    for c, i in enumerate(grid):
        if player in i and cpu not in i:
            for d, j in enumerate(i):
                if j == " ": weights[c][d] += i.count(player) ** 2

        if cpu in i and player not in i:
            for d, j in enumerate(i):
                if j == " ": weights[c][d] += i.count(cpu) ** 3 + 0.1

    #columns
    columns = [[grid[j][i] for j in range(3)] for i in range(3)]
    for c, i in enumerate(columns):
        if player in i and cpu not in i:
            for d, j in enumerate(i):
                if j == " ": weights[d][c] += i.count(player) ** 2

        if cpu in i and player not in i:
            for d, j in enumerate(i):
                if j == " ": weights[d][c] += i.count(cpu) ** 3 + 0.1

    #diagonals
    diagonal = [j[c] for c, j in enumerate(grid)]
    if player in diagonal and cpu not in diagonal:
        for i in range(3):
            if diagonal[i] == " ": weights[i][i] += diagonal.count(player) ** 2
    if cpu in diagonal and player not in diagonal:
        for i in range(3):
            if diagonal[i] == " ": weights[i][i] += diagonal.count(cpu) ** 3 + 0.1

    diagonal = [j[2-c] for c, j in enumerate(grid)]
    if player in diagonal and cpu not in diagonal:
        for i in range(3):
            if diagonal[i] == " ": weights[i][2-i] += diagonal.count(player) ** 2
    if cpu in diagonal and player not in diagonal:
        for i in range(3):
            if diagonal[i] == " ": weights[i][2-i] += diagonal.count(cpu) ** 3 + 0.1
    
    # random choice
    mx = max([max(i) for i in weights])
    choices = []
    for i in range(3):
        for j in range(3):
            if weights[i][j] == mx: choices.append([i, j])
    
    from random import choice
    c = choice(choices)
    grid[c[0]][c[1]] = cpu
    
    # debug
    #from time import sleep
    #print('\n'.join([str(i) for i in weights]))
    #sleep(5)


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