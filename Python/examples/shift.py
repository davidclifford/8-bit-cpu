from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0x80)
    label('right')
    mov(B, A)
    out(B)
    ror(A)
    jpc('left')
    jmp('right')
    label('left')
    mov(A, 1)
    label('loop')
    mov(B, A)
    out(B)
    rol(A)
    jpc('start')
    jmp('loop')

    end(os.path.dirname(__file__)+'/shift')


