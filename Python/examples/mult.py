from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    mov(A, 6)
    mov(B, 7)
    st(A, 'C')
    st(B, 'D')
    mov(A, 0)
    mov(B, 8)
    st(A, 'A')
    st(B, 'B')
    label('loop')
    ld(A, 'A')
    rol(A)
    st(A, 'A')
    ld(B, 'C')
    rol(B)
    st(B, 'C')
    jpc('add-a-d')
    jmp('skip')
    label('add-a-d')
    ld(A, 'A')
    ld(B, 'D')
    add(A, B)
    out(A)
    st(A, 'A')
    label('skip')
    ld(B, 'B')
    dec(B)
    st(B, 'B')
    jpz('end')
    jmp('loop')
    label('end')
    ld(A, 'A')
    out(A)
    label('halt')
    jmp('halt')

    org(0x0)
    var('A')
    var('B')
    var('C')
    var('D')

    end(os.path.dirname(__file__)+'/mult')

# C_Time_D:
# ;Outputs:
# ;     A is the result
# ;     B is 0
#      ld b,8          ;7           7
#      xor a           ;4           4
#        rlca          ;4*8        32
#        rlc c         ;8*8        64
#        jr nc,$+3     ;(12|11)    96|88
#          add a,d     ;--
#        djnz $-6      ;13*7+8     99
#      ret             ;10         10
# ;304+b (b is number of bits)
# ;308 is average speed.
# ;12 bytes