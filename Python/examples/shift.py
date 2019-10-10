from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0x80)
    mov(B, 0)
    label('loop')
    rol(A)
    rol(B)
    jmp('loop')

    end(__file__)


