from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    mov(B, 0)
    label('start')
    dec(B)
    out(B)
    jnz('start')
    hlt()

    end(__file__)


