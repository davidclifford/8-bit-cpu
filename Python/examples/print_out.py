from Python.assembler.asm import *
if __name__ == '__main__':

    def nl():
        jpo()
        out(0xA)
        jpo()
        out(0xD)

    def prnt(char):
        jpo()
        out(char)

    num_chars = 32

    begin()

    nop()
    sp(0)
    prnt(0xC)

    label('start')
    prnt(0x1B)  # ESC
    prnt('[')
    prnt('2')
    prnt('0')
    prnt(';')
    prnt('0')
    prnt('1')
    prnt('f')

    mov(C, 1)
    label('loop2')
    mov(B, C)
    label('loop')

    mov(A, 64)
    add(A, B)
    prnt(A)

    dec(B)
    jnz('loop')
    prnt(0x1B)  # ESC
    prnt('[')
    prnt('A')
    inc(C)
    cmp(C, 20)
    jnz('loop2')
    jmp('start')

    end(__file__)

