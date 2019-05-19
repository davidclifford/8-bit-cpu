from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    label('start')

    mov(B, 'name')
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

    jmp('start')

    org(0x20)
    var('name', 10, 5, 14, 28)

    end(os.path.dirname(__file__)+'/jen')


