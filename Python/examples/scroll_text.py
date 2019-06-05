from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

# init
    nop()
    sp(0xFF)

# Store initial 3 spaces
    mov(D, 0)
    mov(A, 0)
    st(A, D)
    inc(D)
    st(A, D)
    inc(D)
    st(A, D)
    inc(D)

# input from nano until CR
    label('input')
    call('get_char')
    out(A)
    st(A, D)
    inc(D)
    cmp(A, 170)  # CR
    jnz('input')

# add full stop and 3 spaces
    mov(A, 27)  # full stop
    st(A, D)
    inc(D)
    mov(A, 0)
    st(A, D)
    inc(D)
    st(A, D)
    inc(D)
    mov(A, 0xFF)
    st(A, D)

# Scroll text (infinite loop)
    label('scroll')
    mov(C, 0)
    label('loop1')
    mov(D, 15)
    label('loop2')
    mov(B, C)
    call('print4')
    dec(D)
    jnz('loop2')
    inc(C)
    ld(A, C)
    cmp(A, 27)
    jnz('loop1')
    jmp('scroll')

# input from nano into A
    label('get_char')
    in_(A)
    cmp(A, 0)
    jpz('get_char')
    sub(A, 96)
    ret()

# print 4 characters from mem address pointed to by B (destroys A)
    label('print4')
    ld(A, B)
    out(A)
    inc(B)
    ld(A, B)
    or_(A, 0x20)
    out(A)
    inc(B)
    ld(A, B)
    or_(A, 0x40)
    out(A)
    inc(B)
    ld(A, B)
    or_(A, 0x60)
    out(A)
    ret()

    end(__file__)

# ABCDEFGHIJKLMNOPQRSTUVWXYZ.!?_-
#          1111111111222222222233
#01234567890123456789012345678901
