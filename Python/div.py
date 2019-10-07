def rol(ci, cyi):
    cc = ci*2 + cyi
    if cc > 255:
        cc = cc - 256
        return cc, 1
    return cc, 0


if __name__ == '__main__':
    # c/d = c rem a

    c = 34
    d = 0

    a = 0
    b = 8
    cy = 0
    while b > 0:
        c, cy = rol(c, cy)
        a, cy = rol(a, cy)
        if (a - d) >= 0:
            c += 1
            a = a - d
        b = b - 1
        print(a, b, c, d, cy)

    print(c, 'remainder', a, '=', c*d+a)

# ld b, 8
# xor a
#   sla c
#   rla
#   cp d
#   jr c,$+4
#     inc c
#     sub d
#   djnz $-8
# ret
