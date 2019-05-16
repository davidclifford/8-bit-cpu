################
# THE EMULATOR #
################


program = [None for x in range(256)]
A = 0
B = 0
C = 0
D = 0
SP = 0
PC = 0


def load_program(filename):
    global program
    rombin = open(filename, "rb")
    program = rombin.read(256)
    rombin.close()
    for i in range(256):
        print('{:02X}'.format(program[i]))


def run(address):
    global PC
    while True:
        PC = opcode(PC)


def opcode(address):
    global program
    op = program[address]
    perform(op)
    return address + 1

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


def perform(op):
    mask = op & 0xF0
    if mask == 0:
        misc(op)
    elif mask == MOV:
        move(op)
    else:
        print('other')


def misc(op):
    print('misc')


def move(op):
    dd = op & 0x0C >> 2
    ss = op & 0x03
    print('MOV ', dd, ss)


if __name__ == '__main__':
    load_program('fibo.bin')
    run(0)