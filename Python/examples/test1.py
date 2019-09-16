from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0x01)
    mov(B, 0x02)
    mov(C, 0x03)
    mov(D, 0x04)
    out(A)
    out(B)
    out(C)
    out(D)
    add(A, B)
    add(C, D)
    out(A)
    out(C)
    hlt()

    end(__file__)


