from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

# C/D = C rem A
    nop()
    mov(C, 16)
    mov(D, 2)

    mov(A, 0)
    mov(B, 8)

    label('loop1')
    lsl(C)

    rol(A)

    cmp(A, D)
    jnc('loop2')
    inc(C)
    sub(A, D)
    label('loop2')
    dec(B)
    jnz('loop1')
    out(C)
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
