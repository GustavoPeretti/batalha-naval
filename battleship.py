import time

placed = '\u2B1C'
free = '\u2B1B'

check = '\u274E'
wrong = '\u274C'

ships = {
    1: (5, 'Carrier'),
    2: (4, 'Battleship'),
    3: (3, 'Destroyer'),
    4: (3, 'Submarine'),
    5: (2, 'Patrol Boat')
}


def hide():
    print('\n' * 30)


def create_grid():
    return [[free for c in range(grid_size)] for l in range(grid_size)]


def show_grid(grid):
    for l in range(grid_size):
        print(''.join([grid[l][c] for c in range(grid_size)]))


def validate(grid, lco, ship_type):
    size = ships[ship_type][0]
    l, c, o = lco

    def neighbors(l, c):
        neighbors_coords = [
            (l + 1, c),
            (l - 1, c),
            (l, c + 1),
            (l, c - 1),
            (l + 1, c + 1),
            (l - 1, c - 1),
            (l + 1, c - 1),
            (l - 1, c + 1)
        ]

        return [a for a in neighbors_coords if all(0 <= i < grid_size for i in a)]

    def coords(l, c, o):
        if o == 'N':
            coords = [(l - a, c) for a in range(size)]

        if o == 'S':
            coords = [(l + a, c) for a in range(size)]

        if o == 'E':
            coords = [(l, c + a) for a in range(size)]

        if o == 'W':
            coords = [(l, c - a) for a in range(size)]

        return coords

    all_coords = list(coords(l, c, o)) + list(neighbors(l, c))

    return all(0 <= t[n] < grid_size for t in coords(l, c, o) for n in range(2)) and all(
        [grid[pos[0]][pos[1]] == free for pos in all_coords]), lco


def ask_lco(player):
    try:
        lco = input(f'Player {player}, insert line, column and orientation (l - c - o): ').split('-')
        lco[0], lco[1] = int(lco[0]), int(lco[1])
        lco[2] = lco[2].upper().replace(' ', '')
        return lco
    except:
        return ask_lco(player)


def insert(grid, lco, ship_type):
    l, c, o = lco
    size = ships[ship_type][0]

    def coords(l, c, o):
        if o == 'N':
            coords = [(l - a, c) for a in range(size)]

        if o == 'S':
            coords = [(l + a, c) for a in range(size)]

        if o == 'E':
            coords = [(l, c + a) for a in range(size)]

        if o == 'W':
            coords = [(l, c - a) for a in range(size)]

        return coords

    for pos in coords(l, c, o):
        grid[pos[0]][pos[1]] = placed

    return coords(l, c, o)


def rnd(player, grid, ship_type):
    size = ships[ship_type][0]
    show_grid(grid)
    lco = (0, 0, 'N')
    while not validate(grid, lco, size)[0]:
        lco = ask_lco(player)
    return insert(grid, lco, ship_type)


print('=-=' * 30)
print()

print('Welcome to the Battleship game. In the first part, both players will have to position their five types of '
      'ships:\n')

print('Carrier (5)\n'
      'Battleship (4)\n'
      'Destroyer (3)\n'
      'Submarine (2)\n'
      'Patrol Boat (2)\n')

print('After that, the game continues in rounds in which each player will have to guess the positions of a boat and '
      "try to sink them. The player who sinks all the enemy's ships first wins the game.\n")

grid_size = int(input('Type the size of the grid: '))

hide()

grid1 = create_grid()
grid2 = create_grid()

placed1 = dict()
placed2 = dict()

ready = False

player = 1

while not ready:
    for a in range(1, 6):
        placing = set(rnd(player, grid1 if player == 1 else grid2, a))

        if player == 1:
            placed1[a] = placing, set()
        else:
            placed2[a] = placing, set()

        if a == 5:
            show_grid(grid1 if player == 1 else grid2)
            time.sleep(2)
            hide()
    if player == 2:
        ready = True
    player = 2

shot_grid1 = create_grid()
shot_grid2 = create_grid()


def show_both_grids(grid1, grid2):
    for i in range(grid_size):
        print(''.join(grid1[i][j] for j in range(grid_size)) + ' | ' + ''.join(grid2[i][j] for j in range(grid_size)))


def ask_shoot(player):
    try:
        lc = input(f"Player {player}, make a shoot in the enemy's grid (line - column): ").split('-')
        lc[0], lc[1] = int(lc[0]), int(lc[1])
        return tuple(lc)
    except:
        return ask_shoot(player)


def validate_lc(shot_grid, lc):
    l, c = lc
    return shot_grid[l][c] == free


def validate_shot(placed, lc):
    for i in placed.items():
        if lc in i[1][0]:
            return i[0]
    return False


def insert_shot(shot_grid, lc, cond):
    l, c = lc
    if cond:
        shot_grid[l][c] = check
    else:
        shot_grid[l][c] = wrong


def ship_destroyed(placed):
    for i in placed.items():
        if i[1][0] == i[1][1]:
            return i[0]
    return False


def verify_winner(shot_grid1, shot_grid2):
    if sum([shot_grid2[i].count(check) for i in range(grid_size)]) >= 16:
        return 1
    if sum([shot_grid1[i].count(check) for i in range(grid_size)]) >= 16:
        return 2
    return 0


game = True

player = 1

while game:
    if verify_winner(shot_grid1, shot_grid2) == 1:
        show_both_grids(grid1, grid2)
        print('Player 1 won!')
        break
    if verify_winner(shot_grid1, shot_grid2) == 2:
        show_both_grids(grid1, grid2)
        print('Player 2 won!')
        break
    if player == 1:
        show_both_grids(grid1, shot_grid2)
        lc = ask_shoot(player)
        while not validate_lc(shot_grid2, lc):
            lc = ask_shoot(player)
        if validate_shot(placed2, lc):
            print(f'You shot in a {ships[validate_shot(placed2, lc)][1]}')
            insert_shot(shot_grid2, lc, 1)
            for i in placed2.items():
                if lc in i[1][0]:
                    i[1][1].add(lc)
        else:
            insert_shot(shot_grid2, lc, 0)
            print('You shot on the water.')
            player = 2
        sd = ship_destroyed(placed2)
        if sd:
            print(f'The ship {ships[sd][1]} of player 2 was destroyed!')
            del placed2[sd]
            sd = False

    if player == 2:
        show_both_grids(shot_grid1, grid2)
        lc = ask_shoot(player)
        while not validate_lc(shot_grid1, lc):
            lc = ask_shoot(player)
        if validate_shot(placed1, lc):
            print(f'You shot in a {ships[validate_shot(placed1, lc)][1]}')
            insert_shot(shot_grid1, lc, 1)
            for i in placed1.items():
                if lc in i[1][0]:
                    i[1][1].add(lc)
        else:
            insert_shot(shot_grid1, lc, 0)
            print('You shot on the water.')
            player = 2
        sd = ship_destroyed(placed1)
        if sd:
            print(f'The ship {ships[sd][1]} of player 1 was destroyed!')
            del placed1[sd]
            sd = False
