from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    label('start')

    mov(B, 'dave')
    mov(C, 4)
    mov(D, 0)

    label('loop')

    ld(A, B)
    out(A)
    inc(B)
    add(D, 0x10)
    dec(C)

    jpz('start')

    jmp('loop')

    org(0x20)
    var('dave', 4, 1, 22, 5)

    end('dave')
