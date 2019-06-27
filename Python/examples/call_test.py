from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    sp(0)
    mov(A, 1)
    label('loop')
    call('out_a')
    jmp('loop')
    out(2)
    hlt()

    label('out_a')
    out(A)
    ret()

    end(os.path.dirname(__file__)+'/call_test')


