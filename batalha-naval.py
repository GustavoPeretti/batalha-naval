import time

preto = '\u2B1B'
branco = '\u2B1C'
marca = '\u274E'

tipos = {
    1: 'Porta-aviões',
    2: 'Encouraçado',
    3: 'Submarino',
    4: 'Destroyer',
    5: 'Barco de patrulha'
}

tam = {
    1: 5,
    2: 4,
    3: 3,
    4: 3,
    5: 2
}

def hide():
    print('\n' * 100)

def gerar_tab():
    return [[preto for a in range(20)] for a in range(20)]

def mostrar_tab(tab):
    for a in tab:
        for b in a:
            print(b, end='')
        print()
    print()

def mostrar_tabs(tab1, tab2):
    for a in range(20):
        for b in range(20):
            print(tab1[a][b], end='')
        print('', end=' | ')
        for b in range(20):
            print(tab2[a][b], end='')
        print()
    print()


def inserir(tab, tipo, coord, sent, tam, inseridos):
    if tipo in inseridos:
        return False

    size = tam[tipo]

    if sent in 'Nn':
        insert = []
        for a in range(size):

            y = coord[0] - a
            x = coord[1]

            if x < 0 or x > 19 or y < 0 or y > 19 or not tab[y][x] == preto:
                return False
            else:
                insert.append((x, y))

        for a in insert:
            tab[a[1]][a[0]] = branco

    elif sent in 'Ss':
        insert = []
        for a in range(size):
            y = coord[0] + a
            x = coord[1]

            if x < 0 or x > 19 or y < 0 or y > 19 or not tab[y][x] == preto:
                return False
            else:
                insert.append((x, y))

        for a in insert:
            tab[a[1]][a[0]] = branco

    elif sent in 'Ww':
        insert = []
        for a in range(size):
            y = coord[0]
            x = coord[1] - a

            if x < 0 or x > 19 or y < 0 or y > 19 or not tab[y][x] == preto:
                return False
            else:
                insert.append((x, y))

        for a in insert:
            tab[a[1]][a[0]] = branco

    elif sent in 'Ee':
        insert = []
        for a in range(size):
            y = coord[0]
            x = coord[1] + a

            if x < 0 or x > 19 or y < 0 or y > 19 or not tab[y][x] == preto:
                return False
            else:
                insert.append((x, y))

        for a in insert:
            tab[a[1]][a[0]] = branco

    return tab, tipo


def rodada(tam, tipos):
    for a in tam:
        print(f'{a}. {tipos[a]}: {tam[a]}')
    print()

    s = input('Insira (tipo-coordenada-sentido):\n\n').replace(' ', '').split('-')
    s[0] = int(s[0])
    s[1] = tuple(reversed([int(c) for c in s[1].split(',')]))
    s[2] = s[2]

    return s


tab = gerar_tab()
tab2 = gerar_tab()

insert_part = True

inseridos = []

while insert_part:
    hide()
    print('Tabuleiro do jogador 1:\n')
    mostrar_tab(tab)
    i = inserir(tab, *rodada(tam, tipos), tam, inseridos)
    while not i:
        print('Tabuleiro do jogador 1:\n')
        mostrar_tab(tab)
        print('Algo deu errado, insira novamente.')
        i = inserir(tab, *rodada(tam, tipos), tam, inseridos)
    else:
        tab, tipo = i
        inseridos.append(tipo)

    insert_part = not sorted(inseridos) == [1, 2, 3, 4, 5]
hide()
print('Tabuleiro do jogador 1:\n')
mostrar_tab(tab)

time.sleep(1)

insert_part = True

inseridos = []

while insert_part:
    hide()
    print('Tabuleiro do jogador 2:\n')
    mostrar_tab(tab2)
    i = inserir(tab2, *rodada(tam, tipos), tam, inseridos)
    while not i:
        print('Tabuleiro do jogador 2:\n')
        mostrar_tab(tab2)
        print('Algo deu errado, insira novamente.')
        i = inserir(tab2, *rodada(tam, tipos), tam, inseridos)
    else:
        tab2, tipo = i
        inseridos.append(tipo)

    insert_part = not sorted(inseridos) == [1, 2, 3, 4, 5]

hide()
print('Tabuleiro do jogador 2:\n')
mostrar_tab(tab)

time.sleep(1)

game = True

tab_ad = gerar_tab()
tab_ad2 = gerar_tab()

player = 1

def rodada_game(player):
    s = ([-1, -1])
    while any([c < 0 or c > 19 for c in s]):
        s = tuple([int(a) for a in (input(f'Jogador {player}, insira a posição onde deseja lançar a bomba:\n').split(','))])
    return s

def verify_bomb(position, tab):
    return tab[position[1]][position[0]] == branco

while game:
    hide()
    mostrar_tabs(tab_ad, tab_ad2)

    position = rodada_game(player)

    if player == 1:
        if verify_bomb(position, tab2):
            tab_ad2[position[1]][position[0]] = branco
        else:
            tab_ad2[position[1]][position[0]] = marca
            player = 2

    elif player == 2:
        if verify_bomb(position, tab):
            tab_ad[position[1]][position[0]] = branco
        else:
            tab_ad[position[1]][position[0]] = marca
            player = 1

    if sum([tab_ad[a].count(branco) for a in range(20)]) == 17:
        hide()
        mostrar_tabs(tab, tab2)
        print('Jogador 2 venceu!')
        break
    if sum([tab_ad2[a].count(branco) for a in range(20)]) == 17:
        hide()
        mostrar_tabs(tab, tab2)
        print('Jogador 1 venceu!')
        break
