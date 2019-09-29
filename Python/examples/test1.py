from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0x01)
    cmp(A, 0x01)
    jpz('start')
    hlt()

    end(__file__)


