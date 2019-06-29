from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    sp(0xFF)
    label('start')

    mov(C, 'string')

    label('loop1')

    mov(D, 0x11)

    label('loop2')

    mov(B, C)
    call('print4')
    dec(D)
    jnz('loop2')

    inc(C)
    cmp(C, 0x30)
    jpz('start')
    jmp('loop1')

    label('print4')
    lda(B)
    out(A)

    inc(B)
    lda(B)
    or_(A, 0x20)
    out(A)

    inc(B)
    lda(B)
    or_(A, 0x40)
    out(A)

    inc(B)
    lda(B)
    or_(A, 0x60)
    out(A)

    ret()

    org(0x20)
    var('string', 0, 0, 0, 8, 5, 12, 12, 15, 0, 21, 15, 18, 12, 4, 0, 0, 0)

    end(__file__)

# ABCDEFGHIJKLMNOPQRSTUVWXYZ
#          1111111111222222222233
#01234567890123456789012345678901
