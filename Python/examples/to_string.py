from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    # Init
    mov(C, 4)
    mov(D, 2)
    # Divide C by D
    mov(B, 8)
    mov(A, 0)
    label('loop')
    lsl(C)
    rol(A)
    cmp(A, D)
    jpc('skip')
    inc(C)
    sub(A, D)
    label('skip')
    dec(B)
    jnz('loop')
    label('exit')
    out(C)
    hlt()

    end(__file__)
