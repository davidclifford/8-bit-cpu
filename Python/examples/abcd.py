from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0x01)
    mov(B, 0x02)
    add(A, B)
    out(A)
    jmp('loop')

    end(__file__)


