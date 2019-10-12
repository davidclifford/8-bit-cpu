from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    equ('result1', 1)
    equ('result0', 0)

# C/D = C rem A
    nop()
    mov(C, 0x10)
    st(C, 'result1')
    mov(C, 0xE1)
    st(C, 'result0')
    mov(D, 10)

    mov(A, 0)
    mov(B, 16)

    label('loop1')

    ld(C, 'result0')
    lsl(C)
    st(C, 'result0')
    ld(C, 'result1')
    rol(C)
    st(C, 'result1')

    rol(A)

    cmp(A, D)
    jnc('loop2')
    ld(C, 'result0')
    inc(C)
    st(C, 'result0')
    jnc('lower')
    ld(C, 'result1')
    inc(C)
    st(C, 'result1')
    label('lower')

    sub(A, D)
    label('loop2')
    dec(B)
    jnz('loop1')

    ld(C, 'result1')
    out(C)
    ld(D, 'result0')
    out(D)
    hlt()



    end(__file__)

# c/d = c rem a
#
# c = 34
# d = 0
#
# a = 0
# b = 8
# cy = 0
# while b > 0:
#     c, cy = rol(c, cy)
#     a, cy = rol(a, cy)
#     if (a - d) >= 0:
#         c += 1
#         a = a - d
#     b = b - 1
#     print(a, b, c, d, cy)
#
# print(c, 'remainder', a, '=', c * d + a)
