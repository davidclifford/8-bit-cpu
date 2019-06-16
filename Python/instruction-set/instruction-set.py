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
FL = uint32(1) << 22  # ALU Load flags reg from ALU
HL = uint32(1) << 23  # Halt CPU (not needed?)

CI = uint32(1) << 24  # C reg in
CO = uint32(1) << 25  # C reg out
DI = uint32(1) << 26  # D reg in
DO = uint32(1) << 27  # D reg out
SI = uint32(1) << 28  # Stack Pointer in
SO = uint32(1) << 29  # Stack Pointer out
IO = uint32(1) << 30  # Input reg out
MO = uint32(1) << 31  # ROM out

OPERAND = PO | MI
FETCH = PO | MI | IL | PC

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

LDM = 0xD8  # Load from ROM memory into register rr e.g. LDM rr,(#addr)
LDA = 0xDC  # Load A reg from ROM memory addressed by a register e.g. LDA (rr)

LSL = 0xE0
LSR = 0xE4
ROL = 0xE8
ROR = 0xEC

JMP = 0xF0
JPZ = 0xF1
JPN = 0xF2
JPV = 0xF3
JPC = 0xF4
JNZ = 0xF5
JNN = 0xF6
JNV = 0xF7
JNC = 0xF8
OUTI = 0xF9
# 0xFA
HLT = 0xFB
JPR = 0xFC  # - 0xFF


# print("{:08X}".format(IL|PO|PC|MI|HL))

instr: uint32 = [[[0 for i in range(4)] for t in range(8)] for f in range(256)]


def flip_bits(instruction: uint32) -> uint32:
    instruction ^= (IL|RO|XI|YI|EO|MI|PO| AI|AO|BI|BO|JP|OI|TR| FL| CI|CO|DI|DO|SI|SO|IO|MO)
    return instruction


def _r(ss):
    r = (AO, BO, CO, DO)[ss]
    return r


def _w(dd):
    r = (AI, BI, CI, DI)[dd]
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
    instr[address][t][f] = instr[address][t][f] | TR
    for bl in range(t+1, 8):
        instr[address][bl][f] = TR


def instruction_c(address, carry, *micro):
    instruction_c_f(address, carry, False, *micro)
    instruction_c_f(address, carry, True, *micro)


def instruction(address, *micro):
    instruction_c(address, False, *micro)
    instruction_c(address, True, *micro)


def binary_instructions():
    print('Creating binary instructions')
    for dd in range(4):
        for ss in range(4):
            if dd == ss:
                instruction(MOV | dd << 2 | ss, OPERAND, MO | _w(dd))
                instruction(LD | dd << 2 | ss, OPERAND, MO | MI, RO | _w(dd))
                instruction(ST | dd << 2 | ss, OPERAND, MO | MI, RI | _r(dd))
                instruction(ADD | dd << 2 | ss, OPERAND, MO | YI, _r(dd) | XI, ALU_ADD | EO | _w(dd) | FL)
                instruction_c(ADC | dd << 2 | ss, False, OPERAND, MO | YI, _r(dd) | XI, ALU_ADD | EO | _w(dd) | FL)
                instruction_c(ADC | dd << 2 | ss, True, OPERAND, MO | YI, _r(dd) | XI, ALU_ADD | CY | EO | _w(dd) | FL)
                instruction(SUB | dd << 2 | ss, OPERAND, MO | YI, _r(dd) | XI, ALU_SUB | CY | EO | _w(dd) | FL)
                instruction_c(SBB | dd << 2 | ss, False, OPERAND, MO | YI, _r(dd) | XI, ALU_SUB | CY | EO | _w(dd) | FL)
                instruction_c(SBB | dd << 2 | ss, True, OPERAND, MO | YI, _r(dd) | XI, ALU_SUB | EO | _w(dd) | FL)
                instruction(AND | dd << 2 | ss, OPERAND, MO | YI, _r(dd) | XI, ALU_AND | EO | _w(dd) | FL)
                instruction(OR | dd << 2 | ss, OPERAND, MO | YI, _r(dd) | XI, ALU_OR | EO | _w(dd) | FL)
                instruction(XOR | dd << 2 | ss, OPERAND, MO | YI, _r(dd) | XI, ALU_XOR | EO | _w(dd) | FL)
                instruction(CMP | dd << 2 | ss, OPERAND, MO | YI, _r(dd) | XI, ALU_SUB | CY | FL)
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
                instruction(CMP | dd << 2 | ss, _r(ss) | YI, _r(dd) | XI, ALU_SUB | CY | FL)


def unary_instructions():
    print('Creating unary instructions')
    for rr in range(4):
        instruction(NOT | rr, _r(rr) | XI, ALU_SET | EO | YI, ALU_XOR | EO | _w(rr) | FL)
        instruction(NEG | rr, _r(rr) | XI, Y0 | CY | ALU_BSUB | EO | _w(rr) | FL)
        instruction(INC | rr, _r(rr) | XI, Y0 | CY | ALU_ADD | EO | _w(rr) | FL)
        instruction(DEC | rr, _r(rr) | XI, Y0 | ALU_SUB | EO | _w(rr) | FL)
        instruction(IN | rr, IO | _w(rr))
        instruction(OUT | rr, _r(rr) | OI)
        instruction(OUTI | rr, OPERAND, MO | OI)
        instruction(LSL | rr, _r(rr) | XI | YI, ALU_ADD | EO | _w(rr) | FL)
        instruction(LSR | rr, _r(rr) | RV | XI | YI, ALU_ADD | EO | _w(rr) | FL,
                    _r(rr) | RV | XI, Y0 | ALU_ADD | EO | _w(rr))
        instruction_c(ROL | rr, False, _r(rr) | XI | YI, ALU_ADD | FL, ALU_ADD | EO | _w(rr) | FL)
        instruction_c(ROL | rr, True, _r(rr) | XI | YI, ALU_ADD | FL, CY | ALU_ADD | EO | _w(rr) | FL)
        instruction_c(ROR | rr, False, _r(rr) | RV | XI | YI, ALU_ADD | FL,
                      ALU_ADD | EO | _w(rr) | FL, _r(rr) | RV | XI, Y0 | ALU_ADD | EO | _w(rr))
        instruction_c(ROR | rr, True, _r(rr) | RV | XI | YI, CY | ALU_ADD | FL,
                      CY | ALU_ADD | EO | _w(rr) | FL, _r(rr) | RV | XI, Y0 | ALU_ADD | EO | _w(rr))

        instruction(CALR | rr, SO | XI, Y0 | ALU_SUB | EO | SI | MI, PO | RI, _r(rr) | JP)
        instruction(PUSH | rr, SO | XI, Y0 | ALU_SUB | EO | SI | MI, _r(rr) | RI)
        instruction(POP | rr, SO | MI | XI, Y0 | CY | ALU_ADD | EO | SI, RO | _w(rr))
        instruction(JPR | rr, _r(rr) | JP)
        instruction(LDM | rr, OPERAND, MO | MI, MO | _w(rr))
        instruction(LDA | rr, _r(rr) | MI, MO | AI)


def other_instructions():
    print('Creating all other instructions')
    # nop hlt
    instruction(NOP, TR)
    instruction(HLT, PO | XI, Y0 | ALU_SUB | EO | JP)  # jump back to same address!
    # jump
    instruction(JMP, OPERAND, MO | JP)
    instruction_c(JPC, True, OPERAND, MO | JP)
    # instruction_c(JPC, False, PC)
    instruction_c_f(JPZ, True, True, OPERAND, MO | JP)
    instruction_c_f(JPZ, False, True, OPERAND, MO | JP)
    # instruction_c_f(JPZ, True, False, PC)
    # instruction_c_f(JPZ, False, False, PC)
    instruction_c_f(JPN, True, True, OPERAND, MO | JP)
    instruction_c_f(JPN, False, True, OPERAND, MO | JP)
    # instruction_c_f(JPN, True, False, PC)
    # instruction_c_f(JPN, False, False, PC)
    instruction_c_f(JPV, True, True, OPERAND, MO | JP)
    instruction_c_f(JPV, False, True, OPERAND, MO | JP)
    # instruction_c_f(JPV, True, False, PC)
    # instruction_c_f(JPV, False, False, PC)

    instruction_c(JNC, False, OPERAND, MO | JP)
    # instruction_c(JNC, True, PC)
    instruction_c_f(JNZ, True, False, OPERAND, MO | JP)
    instruction_c_f(JNZ, False, False, OPERAND, MO | JP)
    # instruction_c_f(JNZ, True, True, PC)
    # instruction_c_f(JNZ, False, True, PC)
    instruction_c_f(JNN, True, False, OPERAND, MO | JP)
    instruction_c_f(JNN, False, False, OPERAND, MO | JP)
    # instruction_c_f(JNN, True, True, PC)
    # instruction_c_f(JNN, False, True, PC)
    instruction_c_f(JNV, True, False, OPERAND, MO | JP)
    instruction_c_f(JNV, False, False, OPERAND, MO | JP)
    # instruction_c_f(JNV, True, True, PC)
    # instruction_c_f(JNV, False, True, PC)
    # stack based
    instruction(SP, OPERAND, MO | SI)
    instruction(CALL, SO | XI, Y0 | ALU_SUB | EO | SI | MI, PO | RI, PO | MI, MO | JP)
    instruction(RET, SO | MI | XI, RO | JP, Y0 | CY | ALU_ADD | EO | SI)


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


def print_control_all():
    for i in range(256):
        for f in range(4):
            line = "{:02X}".format(i) + ' ' + ('cf', 'cF', 'Cf', 'CF')[f] + ' '
            for t in range(8):
                # flipped = flip_bits(instr[i][t][f])
                # print("{:08X}".format(flipped))
                line = line + get_control(instr[i][t][f]) + ','
            print(line)
        print()

        
def save_all_4_bin():
    print("Saving as 4 roms")
    rom0 = bytearray()
    rom1 = bytearray()
    rom2 = bytearray()
    rom3 = bytearray()
    for i in range(256):
        for t in range(8):
            for f in range(4):
                rom0.append(flip_bits(instr[i][t][f]) & 0xFF)
                rom1.append((flip_bits(instr[i][t][f]) >> 8) & 0xFF)
                rom2.append((flip_bits(instr[i][t][f]) >> 16) & 0xFF)
                rom3.append((flip_bits(instr[i][t][f]) >> 24) & 0xFF)

    rom0bin = open("rom0.bin", "wb")
    rom1bin = open("rom1.bin", "wb")
    rom2bin = open("rom2.bin", "wb")
    rom3bin = open("rom3.bin", "wb")

    rom0bin.write(rom0)
    rom1bin.write(rom1)
    rom2bin.write(rom2)
    rom3bin.write(rom3)

    rom0bin.close()
    rom1bin.close()
    rom2bin.close()
    rom3bin.close()
    print("Finished")


def get_control(part: uint32):
    c = ""
    if part & IL: c += "IL|"
    if part & RO: c += "RO|"
    if part & XI: c += "XI|"
    if part & YI: c += "YI|"
    if part & EO: c += "EO|"
    if part & MI: c += "MI|"
    if part & PC: c += "PC|"
    if part & PO: c += "PO|"

    if part & AI: c += "AI|"
    if part & AO: c += "AO|"
    if part & BI: c += "BI|"
    if part & BO: c += "BO|"
    if part & RI: c += "RI|"
    if part & JP: c += "JP|"
    if part & OI: c += "OI|"
    if part & TR: c += "TR|"

    if part & S0: c += "S0|"
    if part & S1: c += "S1|"
    if part & S2: c += "S2|"
    if part & CY: c += "CY|"
    if part & Y0: c += "Y0|"
    if part & RV: c += "RV|"
    if part & FL: c += "FL|"
    if part & HL: c += "HL|"

    if part & CI: c += "CI|"
    if part & CO: c += "CO|"
    if part & DI: c += "DI|"
    if part & DO: c += "DO|"
    if part & SI: c += "SI|"
    if part & SO: c += "SO|"
    if part & IO: c += "IO|"
    if part & MO: c += "MO|"

    return c


def init_all_nop():
    print('Intitialise all instructions to NOPs')
    for i in range(256):
        for f in range(4):
            instr[i][0][f] = FETCH
            instr[i][1][f] = TR


def read(ser):
    out = ""
    print('xxxxx')
    i = ser.read(256)
    print('i', i)
    out = out + i
    print('out', out)
    return out


def send_command(command, ser, sio):
    com = bytes(command + '\n', 'utf-8')
    ser.write(com)
    time.sleep(0.03)


def setup_serial():
    with serial.Serial('COM7', 115200, timeout=1) as ser:
        print(ser)
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        go = False
        while go is not True:
            time.sleep(0.1)
            send_command('G', ser, sio)
            message = sio.read(256)
            print('MESSAGE ', message)
            if message == 'GO\n':
                go = True

        for i in range(1):
            address = "S{:04X}".format(i*256)
            print(address)
            time.sleep(0.2)
            send_command(address, ser, sio)
            for b in range(8192):
                bite = "{:02X}".format(0xFF-(b & 0xFF))
                send_command(bite, ser, sio)
            send_command('.', ser, sio)

        for i in range(256):
            address = "R{:04X}".format(i*32)
            send_command(address, ser, sio)
            send_command('', ser, sio)
            cont = True
            while cont:
                message = sio.readline(256)
                if len(message) > 0:
                    print('>', message.replace('\n', ''))
                else:
                    cont = False


def main():

    # setup_serial()

    init_all_nop()
    binary_instructions()
    unary_instructions()
    other_instructions()

    # print_all()
    # dump_all()
    print_control_all()
    save_all_4_bin()


if __name__ == '__main__':
    main()
