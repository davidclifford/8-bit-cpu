from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    label('start')
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

    end(os.path.dirname(__file__)+'/mem_test')


