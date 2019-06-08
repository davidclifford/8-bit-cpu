from Python.assembler.asm import *
if __name__ == '__main__':
    begin()
    nop()
    sp(0)

    call('init_board')
    label('next_go')

    call('print_board')
    call('get_input')
    call('print_board')
    call('comp_go')
    call('win?')
    jnz('next_go')

    label('stop')
    jmp('stop')

    # shows players pieces
    label('show_game')
    mov(B, 'home')
    ret()

    # gets next move
    label('get_input')
    ret()

    # computers move
    label('comp_go')
    ret()

    # has someone won?
    label('win?')
    mov(A, 0)
    cmp(A, 0)
    ret()

    # prints out board. Destroys a,b
    label('print_board')
    mov(B, 'home')
    call('print_line')
    mov(B, 'top')
    call('print_player_line')
    mov(B, 'lin')
    call('print_line')
    mov(B, 'mid')
    call('print_player_line')
    mov(B, 'lin')
    call('print_line')
    mov(B, 'bot')
    call('print_player_line')
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
    mov(A, 10)
    out(A)
    mov(A, 13)
    out(A)
    ret()

    # print line. b=address. Destroys a,b
    label('print_player_line')

    # print out B+49 (the number) or X or O

    # print newline
    mov(A, 10)
    out(A)
    mov(A, 13)
    out(A)
    ret()

    label('init_board')
    mov(A, 0)
    mov(B, 9)
    mov(C, 'board')
    label('ib_loop')
    st(A, C)
    inc(C)
    dec(B)
    jnz('ib_loop')
    ret()

    equ('board', 0)
    equ('top', 0)
    equ('mid', 3)
    equ('bot', 6)

    org(0x80)
    var('lin', '#####')
    var('nl', '')
    var('home', 27, 91, 72, 0)
    end(__file__)
