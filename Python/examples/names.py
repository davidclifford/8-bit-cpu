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
    var('name', 20, 15, 14, 25)

    end(os.path.dirname(__file__)+'/tony')


