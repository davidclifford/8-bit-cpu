from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    mov(A, 1)
    mov(B, 2)
    mov(C, 3)
    mov(D, 4)

    mov(D, A)
    mov(C, D)
    mov(B, C)
    mov(A, B)

    hlt()
    end(__file__)
