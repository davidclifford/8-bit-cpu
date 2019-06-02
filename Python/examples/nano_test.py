from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 13)
    out(A)
    mov(A, 0x20)
    label('loop')
    out(A)
    inc(A)
    cmp(A, 0x80)
    jnz('loop')
    jmp('start')

    end(os.path.dirname(__file__)+'/nano_test')


