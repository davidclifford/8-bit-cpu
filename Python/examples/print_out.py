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
    # nl()
    prnt(0xC)
    mov(A, 32)
    mov(B, A)
    sub(B, 31)
    label('next char')
    prnt(A)
    dec(B)
    jpc('next char')
    nl()
    mov(B, A)
    sub(B, 31)
    inc(A)
    cmp(A, 0x5a)
    jnz('next char')
    jmp('start')

    end(__file__)

