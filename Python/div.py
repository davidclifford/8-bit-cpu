if __name__ == '__main__':
    # c/d = c rem a

    c = 35
    d = 10

    a = 0
    b = 8

    print(c, a)
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