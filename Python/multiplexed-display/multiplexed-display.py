#
# This is an improved 8-bit
# decimal display for an 8-bit CPU
#

rom = [0 for _ in range(8192)]

D0 = 0x0
D1 = 0x100
D2 = 0x200
D3 = 0x300
NEGATIVE = 0x400
HEXA = 0x800
OCTAL = 0xC00
ALPHA = 0x1000
DASCII = 0x2000

BLANK = 0x0
NEG = 0x1
LTR_H = 0x37
LTR_O = 0x1d


def set_rom(address, value):
    rom[address] = value


def digit(val, place, div):

    digits = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b]  # with 0 for zero

    value = val
    p = place & 0x3FF
    _digit = digits[abs(int(value/div)) % 10]

    if value >= 0:
        if value < 10 and p == D1:
            _digit = BLANK
        if value < 100 and p == D2:
            _digit = BLANK
        if p == D3:
            _digit = BLANK
    else:
        if abs(value) < 10 and p == D1:
            _digit = NEG if value < 0 else BLANK
        if abs(value) < 100 and p == D2:
            _digit = NEG if value <= -10 else BLANK
        if p == D3:
            _digit = NEG if value <= -100 else BLANK

    return _digit


def main():
    print("Programming unsigned numbers")
    for value in range(256):
        set_rom(value | D0, digit(value, D0, 1))
        set_rom(value | D1, digit(value, D1, 10))
        set_rom(value | D2, digit(value, D2, 100))
        set_rom(value | D3, digit(value, D3, 1))

    print("Programming signed numbers")
    for value in range(-128,128):
        set_rom(value | NEGATIVE | D0, digit(value, D0, 1))
        set_rom(value | NEGATIVE | D1, digit(value, D1, 10))
        set_rom(value | NEGATIVE | D2, digit(value, D2, 100))
        set_rom(value | NEGATIVE | D3, digit(value, D3, 1))

    #  hexa[] = { 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b, 0x7d, 0x1f, 0x0d, 0x3d, 0x6f, 0x47} # lowercase
    hexa = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b, 0x77, 0x1f, 0x4e, 0x3d, 0x4f, 0x47]  # uppercase
    print("Programming hex numbers")
    for value in range(256):
        set_rom(value | HEXA | D0, hexa[value % 16])
        set_rom(value | HEXA | D1, hexa[int(value / 16) % 16])
        set_rom(value | HEXA | D2, BLANK)
        set_rom(value | HEXA | D3, LTR_H)

    # digits[] = { 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70} # 0-7
    print("Programming octal numbers")
    for value in range(256):
        set_rom(value | OCTAL | D0, hexa[(value % 8)])
        set_rom(value | OCTAL | D1, hexa[int(value / 8) % 8])
        set_rom(value | OCTAL | D2, hexa[int(value / 64) % 8])
        set_rom(value | OCTAL | D3, LTR_O)

    # ALPHA
    letters = [BLANK, 0x7d, 0x1f, 0x0d, 0x3d, 0x6f, 0x47, 0x7b,  # space, a-g
               0x17, 0x50, 0x58, 0x37, 0x0e, 0x4f, 0x15, 0x1d,  # h-o
               0x67, 0x73, 0x05, 0x5b, 0x0f, 0x1c, 0x0c, 0x79,  # p-w
               0xB7, 0x3b, 0x6d, 0x80, 0xb0, 0xe5, 0x08, 0x01]  # x-z, . ! ? _ -
    print("Programming alpha")
    for disp in range(8):
        for value in range(32):
            let1 = BLANK
            let2 = BLANK
            let3 = BLANK
            let4 = BLANK
            if disp % 4 == 0:
                let1 = letters[value]
            if disp % 4 == 1:
                let2 = letters[value]
            if disp % 4 == 2:
                let3 = letters[value]
            if disp % 4 == 3:
                let4 = letters[value]
            set_rom(value + disp * 32 | ALPHA | D3, let1)
            set_rom(value + disp * 32 | ALPHA | D2, let2)
            set_rom(value + disp * 32 | ALPHA | D1, let3)
            set_rom(value + disp * 32 | ALPHA | D0, let4)

    # DASCII
    chars = [BLANK, 0xb0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # _!"#$%&'
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # # ()*+,-./
              0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70,  # 0-7
              0x7f, 0x7b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  # 8-9 :;<=>?
              0x00, 0x7d, 0x1f, 0x0d, 0x3d, 0x6f, 0x47, 0x7b,  # @, a-g
              0x17, 0x50, 0x58, 0x37, 0x0e, 0x4f, 0x15, 0x1d,  # h-o
              0x67, 0x73, 0x05, 0x5b, 0x0f, 0x1c, 0x0c, 0x79,  # p-w
              0xB7, 0x3b, 0x6d, 0x80, 0xb0, 0xe5, 0x08, 0x01]  # x-z, [\]^_
    print("Programming alpha")
    for disp in range(8):
        for value in range(64):
            let1 = BLANK
            let2 = BLANK
            let3 = BLANK
            let4 = BLANK
            if disp % 4 == 0:
                let1 = chars[value]
            if disp % 4 == 1:
                let2 = chars[value]
            if disp % 4 == 2:
                let3 = chars[value]
            if disp % 4 == 3:
                let4 = chars[value]
            set_rom(value + disp * 64 | DASCII | D3, let1)
            set_rom(value + disp * 64 | DASCII | D2, let2)
            set_rom(value + disp * 64 | DASCII | D1, let3)
            set_rom(value + disp * 64 | DASCII | D0, let4)

    dump()
    save_bin('display.bin')


def save_bin(filename):
    print("\nSaving {:s} as binary file".format(filename))
    rom_bin = bytearray()
    for i in range(len(rom)):
        rom_bin.append(rom[i] or 0)
    rom_image = open(filename, "wb")
    rom_image.write(rom_bin)
    rom_image.close()


def dump():
    for i in range(0, len(rom), 8):
        print("{:04X}: {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}"
              .format(i, rom[i], rom[i+1], rom[i+2], rom[i+3], rom[i+4], rom[i+5], rom[i+6], rom[i+7]))


if __name__ == '__main__':
    main()
