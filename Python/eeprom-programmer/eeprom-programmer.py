from numpy import uint32

IL = uint32(1) << 0  # Instruction reg load (from ROM)
RO = uint32(1) << 1  # Ram out
XI = uint32(1) << 2  # ALU X in
YI = uint32(1) << 3  # ALU Y in
EO = uint32(1) << 4  # ALU result out
MI = uint32(1) << 5  # Mem address in
PC = uint32(1) << 6  # Prog count increment
PO = uint32(1) << 7  # Prog counter out

AI = uint32(1) << 8  # A reg in
AO = uint32(1) << 9  # A reg out
BI = uint32(1) << 10  # B reg in
BO = uint32(1) << 11  # B reg out
RI = uint32(1) << 12  # Ram in
JP = uint32(1) << 13  # Jump (PC in)
OI = uint32(1) << 14  # Output in (display)
TR = uint32(1) << 15  # Reset T states

S0 = uint32(1) << 16  # ALU setting 0
S1 = uint32(1) << 17  # ALU setting 1
S2 = uint32(1) << 18  # ALU setting 2
CY = uint32(1) << 19  # ALU Carry in
Y0 = uint32(1) << 20  # ALU Y zero
RV = uint32(1) << 21  # ALU Reverse bits into X&Y
FL = uint32(1) << 21  # ALU Load flags reg from ALU
MO = uint32(1) << 23  # ROM out

CI = uint32(1) << 24  # C reg in
CO = uint32(1) << 25  # C reg out
DI = uint32(1) << 26  # D reg in
DO = uint32(1) << 27  # D reg out
SI = uint32(1) << 28  # Stack Pointer in
SO = uint32(1) << 29  # Stack Pointer out
DM = uint32(1) << 30  # Display mode in (dec/signed/hex/octal/dascii)
HL = uint32(1) << 31  # Halt CPU (not needed?)

OPERAND = PO | MI | PC
FETCH = OPERAND | IL

# print("{:08X}".format(IL|PO|PC|MI|HL))

instr = [[[0 for i in range(4)] for t in range(8)] for f in range(256)]


def flip_bits(instruction: uint32) -> uint32:
    instruction ^= (IL|RO|XI|YI|EO|MI|PO| AI|AO|BI|BO|JP|OI|TR| FL| CI|CO|DI|DO|SI|SO|DM)
    return instruction


def _r(ss):
    r = (AI, BI, CI, DI)[ss]
    return r


def _w(dd):
    r = (AO, BO, CO, DO)[dd]
    return r


# ss dd rr 00 A 01 B 10 C
def instruction(addr, *micro):
    for f in range(4):
        instr[addr][0][f] = FETCH
    i = 0
    for m in micro:
        i += 1
        for f in range(4):
            instr[addr][i][f] = m
    instr[addr][i][0] = instr[addr][i][0] | TR
    for bl in range(i+1, 8):
        for f in range(4):
            instr[addr][bl][f] = 0


def print_all():
    for i in range(256):
        print('instruction: '+'{:02X}'.format(i))
        for t in range(8):
            print("{:08X}".format(instr[i][t][0]))
        print()


def init_all_nop():
    for i in range(256):
        for f in range(4):
            instr[i][0][f] = FETCH | TR


def main():
    init_all_nop()

    # move instructions 0x10
    for dd in range(4):
        for ss in range(4):
            if dd == ss:
                instruction(0x00 | dd << 2 | ss, OPERAND, RO | _w(dd))
            else:
                instruction(0x00 | dd << 2 | ss, _r(ss) | _w(dd))

    print_all()


main()
