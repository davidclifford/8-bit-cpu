from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    mov(A, 0)
    mov(B, 0xFF)
    label('start')
    in_(A)
    # xor(A, B)
    jmp('start')
    end(__file__)


