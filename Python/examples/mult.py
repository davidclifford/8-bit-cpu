from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    sp(0xFF)
    label('for a')
    mov(A, 1)
    label('for b')
    mov(B, 1)
    label('b loop')
    mov(C, A)
    mov(D, B)
    push(A)
    push(B)
    call('mult')
    out(A)
    pop(B)
    pop(A)
    inc(B)
    cmp(B, 16)
    jnz('b loop')
    inc(A)
    cmp(A, 16)
    jnz('for b')
    jmp('for a')
    hlt()

    label('mult')
    mov(A, 0)
    mov(B, 8)
    label('loop')
    rol(A)
    rol(C)
    jpc('add-a-d')
    jmp('skip')
    label('add-a-d')
    add(A, D)
    label('skip')
    dec(B)
    jpz('end')
    jmp('loop')
    label('end')
    ret()

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