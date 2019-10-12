from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    equ('a', 0)
    equ('b', 1)

    nop()
    label('start')
    mov(C, 0x17)
    st(C, 'a')
    mov(C, 0x35)
    st(C, 'b')
    mov(C, 0xFF)
    ld(C, 'b')
    out(C)
    hlt()

    mov(A, 0xFF)
    mov(B, 0x00)
    label('loop')
    inc(B)
    dec(A)
    out(B)
    st(A, B)
    ld(C, B)
    cmp(A, C)
    jpz('loop')
    hlt()



    end(__file__)


