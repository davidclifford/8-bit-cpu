import keyboard
from Python.assembler.asm import *
if __name__ == '__main__':
    begin()
    nop()
    sp(0)

    call('init_board')
    call('print_board')

    label('next_go')
    call('get_input')
    call('print_board')
    call('win?')
    jnz('game_won')
    call('comp_go')
    call('print_board')
    call('win?')
    jpz('next_go')

    label('game_won')
    # print who won
    cmp(A, 1)
    jnz('comp won')
    mov(B, 'you')
    call('print_line')
    jmp('print_won')
    label('comp won')
    mov(B, 'i')
    call('print_line')
    label('print_won')
    mov(B, 'win')
    call('print_line')
    hlt()

    # gets next move
    label('get_input')
    mov(B, 'next_move')
    call('print_line')
    label('gi_loop')
    in_(A)
    cmp(A, 0)
    jpz('gi_loop')
    sub(A, 49)
    mov(B, 'board')
    add(B, A)
    ld(A, B)
    cmp(A, 0)
    jnz('gi_loop')
    mov(A, 1)
    st(A, B)
    ret()

    # computers move
    label('comp_go')
    mov(B, 'board')
    mov(C, 9)
    label('cg_loop')
    ld(A, B)
    cmp(A, 0)
    jpz('cg_found')
    inc(B)
    dec(C)
    cmp(C, 0)
    jnz('cg_loop')
    label('cg_found')
    mov(A, 4)
    st(A, B)
    ret()

    # has someone won?
    label('win?')
    mov(A, 0)
    mov(D, 'score')
    mov(B, 'board')

    call('row3')
    call('row3')
    call('row3')

    ret()

# ROWS
    label('row3')
    call('row')
    st(A, D)
    inc(D)
    call('row')
    st(A, D)
    inc(D)
    call('row')
    st(A, D)
    inc(D)


    label('row')
    ld(C, B)
    add(A, C)
    inc(B)
    ret()

    label('column')
    ld(C, B)
    add(A, C)
    add(B, 3)
    ret()

    label('diag1')
    ld(C, B)
    add(A, C)
    add(B, 4)
    ret()

    label('diag2')
    ld(C, B)
    add(A, C)
    add(B, 2)
    ret()

    cmp(A, 0)
    ret()

    # prints out board. Destroys a,b
    label('print_board')
    mov(B, 'home')
    call('print_line')
    mov(B, 0)
    call('print_player_line')
    mov(B, 'lin')
    call('print_line')
    mov(B, 3)
    call('print_player_line')
    mov(B, 'lin')
    call('print_line')
    mov(B, 6)
    call('print_player_line')
    ret()

    # b =
    label('print_player_line')
    call('print_o_x')
    out(124)
    inc(B)
    call('print_o_x')
    out(124)
    inc(B)
    call('print_o_x')
    # print newline
    out(10)
    out(13)
    ret()

    label('print_o_x')
    ld(A, B)
    cmp(A, 0)
    jnz('ox')
    add(A, B)
    add(A, 49)
    out(A)
    ret()
    label('ox')
    cmp(A, 1)
    jnz('X')
    out(79)
    ret()
    label('X')
    out(88)
    ret()

    # print line. b=address. Destroys a,b
    label('print_line')
    label('pl_loop')
    lda(B)
    cmp(A, 0)
    jpz('pl_done')
    out(A)
    inc(B)
    jmp('pl_loop')
    label('pl_done')
    out(10)
    out(13)
    ret()

    label('init_board')
    mov(A, 0)
    mov(B, 9)
    label('ib_loop')
    dec(B)
    st(A, B)
    jnz('ib_loop')
    ret()

    equ('board', 0)
    equ('top', 0)
    equ('mid', 3)
    equ('bot', 6)
    equ('score', 0x10)

    org(0xDB)
    var('lin', '-+-+-')
    var('home', 27, 91, 72, 0)
    var('next_move', 'Your move? ')
    var('i', 10, 13, 'I')
    var('you', 10, 13, 'You')
    var('win', 'win!')
    end(__file__)


board = [None for _ in range(256)]
a = 0
b = 0
c = 0
d = 0
sp = 255


def pout(char):
    print(char, end='')


def init_board():
    global a, b, board
    a = 0
    b = 0
    while b < 9:
        board[b] = a
        b = b + 1


def print_o_x():
    global a, b, board
    a = board[b]
    b = b + 1
    if a == 1:
        pout('O')
    elif a == 4:
        pout('X')
    else:
        pout(b)


def print_play():
    global a, b, board
    print_o_x()
    pout('|')
    print_o_x()
    pout('|')
    print_o_x()
    pout('\n')


def print_board():
    global a, b, board
    b = 0
    pout('\n\n')
    print_play()
    pout('-+-+-\n')
    print_play()
    pout('-+-+-\n')
    print_play()


def get_input():
    global a
    a = get_key()


def get_key():
    while True:
        if keyboard.is_pressed('1'):
            return 0
        if keyboard.is_pressed('2'):
            return 1
        if keyboard.is_pressed('3'):
            return 2
        if keyboard.is_pressed('4'):
            return 3
        if keyboard.is_pressed('5'):
            return 4
        if keyboard.is_pressed('6'):
            return 5
        if keyboard.is_pressed('7'):
            return 6
        if keyboard.is_pressed('8'):
            return 7
        if keyboard.is_pressed('9'):
            return 8


def player_turn():
    global a, board
    while True:
        print_board()
        pout('Your move? ')
        a = -1
        while a == -1:
            get_input()
            if board[a] != 0:
                a = -1
        board[a] = 1


init_board()
while True:
    print_board()
    player_turn()


