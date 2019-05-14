from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    label('start')

    mov(A, 0)
    mov(B, 1)

    label('next')
    add(B, A)
    mov(A, B)
    sub(A, B)
    out(A)
    jpc('start')
    jmp('next')

    org(0x10)
    var('temp')

    end('fibo2')
