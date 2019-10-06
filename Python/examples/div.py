from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

# C/D = C rem A
    nop()
    sp(0xFF)
    mov(A, 0)
    mov(B, 8)
    lsl(C)
    label('loop1')
    rol(A)
    cmp(A, D)
    jnc('loop2')
    sbb(A, D)
    label('loop2')
    rol(C)
    dec(B)
    jnz('loop1')
    out(C)
    hlt()

    end(__file__)

# ;
#    LDA #0
#    LDX #8
#    ASL TQ
# L1 ROL
#    CMP B
#    BCC L2
#    SBC B
# L2 ROL TQ
#    DEX
#    BNE L1

# ; 8bit/8bit division
# ; by White Flame
# ;
# ; Input: num, denom in zeropage
# ; Output: num = quotient, .A = remainder
#
#  lda #$00
#  ldx #$07
#  clc
# : rol num
#   rol
#   cmp denom
#   bcc :+
#    sbc denom
# : dex
#  bpl :--
#  rol num