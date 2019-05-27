from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0x01)
    mov(B, 0x02)
    mov(C, 0x04)
    mov(D, 0x08)
    label('loop')
    out(A)
    out(B)
    out(C)
    out(D)
    rol(A)
    rol(B)
    rol(C)
    rol(D)
    jmp('loop')

    end(os.path.dirname(__file__)+'/abcd')


