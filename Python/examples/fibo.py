from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    mov(A, 0)
    mov(B, 1)

    label('next')
    st(B, 'temp')
    add(B, A)
    ld(A, 'temp')
    out(A)
    jpc('start')
    jmp('next')
    hlt()

    org(0x10)
    var('temp', 0xFF)

    end(__file__)
