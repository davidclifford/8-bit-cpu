from numpy import uint32
import serial
import io
import time

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
IO = uint32(1) << 30  # Input reg out
HL = uint32(1) << 31  # Halt CPU (not needed?)

OPERAND = PO | MI | PC
FETCH = OPERAND | IL

ALU_CLR = 0
ALU_BSUB = S0
ALU_SUB = S1
ALU_ADD = S0 | S1
ALU_XOR = S2
ALU_OR = S2 | S0
ALU_AND = S2 | S1
ALU_SET = S2 | S1 | S0

NOP = 0x00
SP = 0x01
CALL = 0x02
RET = 0x03

CALR = 0x4
PUSH = 0x8
POP = 0xC

MOV = 0x10
LD = 0x20
ST = 0x30
ADD = 0x40
ADC = 0x50
SUB = 0x60
SBB = 0x70
OR = 0x80
XOR = 0x90
AND = 0xA0
CMP = 0xB0

NOT = 0xC0
NEG = 0xC4
INC = 0xC8
DEC = 0xCC

IN = 0xD0
OUT = 0xD4

XXrr = 0xD8
YYrr = 0xDC

LSL = 0xE0
LSR = 0xE4
ROL = 0xE8
ROR = 0xEC

JMP = 0xF0
JPZ = 0xF1
JPN = 0xF2
# 0xF3
JPV = 0xF4
# 0xF5
# 0xF6
# 0xF7
JPC = 0xF8
# 0xF9
# 0xFA
HLT = 0xFB
JPR = 0xFC


# print("{:08X}".format(IL|PO|PC|MI|HL))

instr = [[[0 for i in range(4)] for t in range(8)] for f in range(256)]


def flip_bits(instruction: uint32) -> uint32:
    instruction ^= (IL|RO|XI|YI|EO|MI|PO| AI|AO|BI|BO|JP|OI|TR| FL| CI|CO|DI|DO|SI|SO|IO)
    return instruction


def _r(ss):
    r = (AI, BI, CI, DI)[ss]
    return r


def _w(dd):
    r = (AO, BO, CO, DO)[dd]
    return r


# ss dd rr 00 A 01 B 10 C
def instruction_c_f(address, carry, flags, *micro):
    f = 1 if flags else 0
    f = f+2 if carry else f
    instr[address][0][f] = FETCH
    t = 0
    for m in micro:
        t += 1
        instr[address][t][f] = m
    instr[address][t][0] = instr[address][t][0] | TR
    for bl in range(t+1, 8):
        instr[address][bl][f] = TR


def instruction_c(address, carry, *micro):
    instruction_c_f(address, carry, False, *micro)
    instruction_c_f(address, carry, True, *micro)


def instruction(address, *micro):
    instruction_c(address, False, *micro)
    instruction_c(address, True, *micro)


def binary_instructions():
    for dd in range(4):
        for ss in range(4):
            if dd == ss:
                instruction(MOV | dd << 2 | ss, OPERAND, RO | _w(dd))
                instruction(LD | dd << 2 | ss, OPERAND, RO | MI, RO | _w(dd))
                instruction(ST | dd << 2 | ss, OPERAND, RI | _r(dd))
                instruction(ADD | dd << 2 | ss, OPERAND, RO | YI, _r(dd) | XI, ALU_ADD | EO | _w(dd) | FL)
                instruction_c(ADC | dd << 2 | ss, False, OPERAND, RO | YI, _r(dd) | XI, ALU_ADD | EO | _w(dd) | FL)
                instruction_c(ADC | dd << 2 | ss, True, OPERAND, RO | YI, _r(dd) | XI, ALU_ADD | CY | EO | _w(dd) | FL)
                instruction(SUB | dd << 2 | ss, OPERAND, RO | YI, _r(dd) | XI, ALU_SUB | CY | EO | _w(dd) | FL)
                instruction_c(SBB | dd << 2 | ss, False, OPERAND, RO | YI, _r(dd) | XI, ALU_SUB | CY | EO | _w(dd) | FL)
                instruction_c(SBB | dd << 2 | ss, True, OPERAND, RO | YI, _r(dd) | XI, ALU_SUB | EO | _w(dd) | FL)
                instruction(AND | dd << 2 | ss, OPERAND, RO | YI, _r(dd) | XI, ALU_AND | EO | _w(dd) | FL)
                instruction(OR | dd << 2 | ss, OPERAND, RO | YI, _r(dd) | XI, ALU_OR | EO | _w(dd) | FL)
                instruction(XOR | dd << 2 | ss, OPERAND, RO | YI, _r(dd) | XI, ALU_XOR | EO | _w(dd) | FL)
                instruction(CMP | dd << 2 | ss, OPERAND, RO | YI, _r(dd) | XI, ALU_SUB | FL)
            else:
                instruction(MOV | dd << 2 | ss, _r(ss) | _w(dd))
                instruction(LD | dd << 2 | ss, _r(ss) | MI, RO | _w(dd))
                instruction(ST | dd << 2 | ss, _r(ss) | MI, RI | _r(dd))
                instruction(ADD | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_ADD | EO | _w(dd) | FL)
                instruction_c(ADC | dd << 2 | ss, False, _r(ss) | YI, _r(dd) | XI, ALU_ADD | EO | _w(dd) | FL)
                instruction_c(ADC | dd << 2 | ss, True, _r(ss) | YI, _r(dd) | XI, ALU_ADD | CY | EO | _w(dd) | FL)
                instruction(SUB | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_SUB | CY | EO | _w(dd) | FL)
                instruction_c(SBB | dd << 2 | ss, False, _r(ss) | YI, _r(dd) | XI, ALU_SUB | CY | EO | _w(dd) | FL)
                instruction_c(SBB | dd << 2 | ss, True, _r(ss) | YI, _r(dd) | XI, ALU_SUB | EO | _w(dd) | FL)
                instruction(AND | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_AND | EO | _w(dd) | FL)
                instruction(OR | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_OR | EO | _w(dd) | FL)
                instruction(XOR | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_XOR | EO | _w(dd) | FL)
                instruction(CMP | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_SUB | FL)


def unary_instructions():
    for rr in range(4):
        instruction(NOT | rr, _r(rr) | XI, ALU_SET | EO | YI, ALU_XOR | EO | _w(rr) | FL)
        instruction(NEG | rr, _r(rr) | XI, Y0 | ALU_BSUB | EO | _w(rr) | FL)
        instruction(INC | rr, _r(rr) | XI, Y0 | CY | ALU_ADD | EO | _w(rr) | FL)
        instruction(DEC | rr, _r(rr) | XI,  Y0 | ALU_SUB | EO | _w(rr) | FL)
        instruction(IN | rr, IO | _w(rr))
        instruction(OUT | rr, _r(rr) | OI)
        instruction(LSL | rr, _r(rr) | XI | YI, ALU_ADD | EO | _w(rr) | FL)
        instruction(LSR | rr, _r(rr) | RV | XI | YI, ALU_ADD | EO | RV | XI | FL, Y0 | ALU_ADD | _w(rr))
        instruction_c(ROL | rr, False, _r(rr) | XI | YI, ALU_ADD | FL, ALU_ADD | EO | _w(rr) | FL)
        instruction_c(ROL | rr, True, _r(rr) | XI | YI, ALU_ADD | FL, CY | ALU_ADD | EO | _w(rr) | FL)
        instruction_c(ROR | rr, False, _r(rr) | RV | XI | YI, ALU_ADD | FL,
                      ALU_ADD | EO | RV | XI | FL, Y0 | ALU_ADD, _w(rr))
        instruction_c(ROR | rr,  True, _r(rr) | RV | XI | YI, ALU_ADD | FL,
                      CY | ALU_ADD | EO | RV | XI | FL, Y0 | ALU_ADD | EO | _w(rr))

        instruction(CALR | rr, SO | XI, Y0 | ALU_SUB | EO | SI | MI, PO | RI, _r(rr) | JP)
        instruction(PUSH | rr, SO | XI, Y0 | ALU_SUB | EO | SI | MI, _r(rr) | RI)
        instruction(POP | rr, SO | MI | XI, Y0 | CY | ALU_ADD | EO | SI, RO | _w(rr))
        instruction(JPR | rr, _r(rr) | JP)


def other_instructions():
    # nop hlt
    instruction(NOP,)
    instruction(HLT, HL)
    # jump
    instruction(JMP, OPERAND, RO | JP)
    instruction_c(JPC, True, OPERAND, RO | JP)
    instruction_c_f(JPZ, True, True, OPERAND, RO | JP)
    instruction_c_f(JPZ, False, True, OPERAND, RO | JP)
    instruction_c_f(JPN, True, True, OPERAND, RO | JP)
    instruction_c_f(JPN, False, True, OPERAND, RO | JP)
    instruction_c_f(JPV, True, True, OPERAND, RO | JP)
    instruction_c_f(JPV, False, True, OPERAND, RO | JP)
    # stack based
    instruction(SP, OPERAND, RO | SI)
    instruction(CALL, SO | XI, Y0 | ALU_SUB | EO | SI | MI, PO | RI, OPERAND, RO | JP)
    instruction(RET, SO | MI | XI, Y0 | CY | ALU_ADD | EO | SI, RO | JP)


def print_all():
    for i in range(256):
        print('instruction: '+'{:02X}'.format(i))
        # for f in range(4):
            # print(('cf', 'cF', 'Cf', 'CF')[f])
        for t in range(8):
            print("{:08X}".format(instr[i][t][0]))
        print()


def dump_all():
    for i in range(256):
        for t in range(8):
            for f in range(4):
                flipped = flip_bits(instr[i][t][f])
                print("{:08X}".format(flipped))


def init_all_nop():
    for i in range(256):
        for f in range(4):
            instr[i][0][f] = FETCH | TR


def read(ser):
    out = ""
    print('xxxxx')
    i = ser.read(256)
    print('i', i)
    out = out + i
    print('out', out)
    return out


def send_command(command, ser, sio):
    while True:
        com = bytes(command + '\n', 'utf-8')
        ser.write(com)
        ret_com = sio.readline(256)
        if ret_com == command+'\n':
            return


def setup_serial():
    with serial.Serial('COM7', 57600, timeout=1) as ser:
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        send_command('G', ser, sio)
        print(sio.readline(256))

        send_command('S', ser, sio)
        message = sio.readline(256)
        print('>', message)

        send_command('R', ser, sio)
        print(sio.readline(256))

def main():

    setup_serial()

    # init_all_nop()
    # binary_instructions()
    # unary_instructions()
    # other_instructions()
    #
    # print_all()
    # dump_all()


main()
