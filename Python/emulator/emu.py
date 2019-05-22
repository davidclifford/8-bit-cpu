################
# THE EMULATOR #
################


program = [None for _ in range(256)]
MEM = [None for _ in range(256)]
A = 0
B = 0
C = 0
D = 0
SP = 0
PC = 0
FLAG_CY = 0
FLAG_ZERO = 0
FLAG_NEG = 0
FLAG_OVER = 0


def load_program(filename):
    global program
    rombin = open(filename, "rb")
    program = rombin.read(256)
    rombin.close()
    # for i in range(256):
    #     print('{:02X}'.format(program[i]))


def run(address):
    global PC
    PC = address
    while True:
        status()
        opcode(PC)
        print()

def opcode(address):
    global program
    op = program[address]
    perform(op)


def operand():
    global program, PC
    inc_pc()
    oper = program[PC]
    return oper


def inc_pc():
    global PC
    PC += 1
    if PC > 255:
        PC = 0
        exit(0)


def jmp_pc(pc):
    global PC
    PC = pc


def result(comp, flags=False):
    global FLAG_CY, FLAG_NEG, FLAG_OVER, FLAG_ZERO
    res = comp
    if flags:
        FLAG_CY = res > 256 or res < 0
    if res > 256:
        res = res - 256
    if res < 0:
        res = res + 256

    if flags:
        FLAG_ZERO = res == 0
        FLAG_NEG = res >= 128

    return res

def _r(ss):
    global A,B,C,D
    if ss == 0:
        return A
    if ss == 1:
        return B
    if ss == 2:
        return C
    if ss == 3:
        return C


def _w(dd, num):
    global A,B,C,D
    if dd == 0:
        A = num
    elif dd == 1:
        B = num
    elif dd == 2:
        C = num
    elif dd == 3:
        D = num


def status():
    global A, B, C, D, SP, PC, FLAG_CY, FLAG_NEG, FLAG_ZERO, FLAG_OVER
    reg = 'A {:02X} B {:02X} C {:02X} D {:02X} SP {:02X} '.format(A, B, C, D, SP)
    flag = 'C' if FLAG_CY else 'c'
    flag = flag + ('Z' if FLAG_ZERO else 'z')
    flag = flag + ('N' if FLAG_NEG else 'n')
    flag = flag + ('V' if FLAG_OVER else 'v')
    pc_flag = 'PC {:02X} {:s}'.format(PC, flag)
    print(pc_flag)
    print(reg)


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
    elif mask == LD:
        ld(op)
    elif mask == ST:
        st(op)
    elif mask == ADD:
        add(op)
    elif mask == ADC:
        adc(op)
    elif mask == SUB:
        sub(op)
    elif mask == SBB:
        sbb(op)
    elif mask == OR:
        or_(op)
    elif mask == XOR:
        xor(op)
    elif mask == AND:
        and_(op)
    elif mask == CMP:
        cmp(op)
    else:
        other(op)


def ddss(op):
    return op & 0x03, op & 0x0C >> 2


def rr(op):
    return op & 0x03


def reg(rr):
    return ['A', 'B', 'C', 'D'][rr]


def misc(op):
    if op == NOP:
        nop(op)
    else:
        print('misc {:02X}'.format(op))
        inc_pc()


def other(op):
    print('other {:02X}'.format(op))
    inc_pc()


def nop(op):
    print('NOP')
    inc_pc()


def move(op):
    dd, ss = ddss(op)
    if dd == ss:
        num = operand()
        _w(dd, num)
        print('MOV ', reg(dd), num)
    else:
        _w(dd, _r(ss))
        print('MOV ', dd, ss)
    inc_pc()


def ld(op):
    dd, ss = ddss(op)
    print('LD ', dd, ss)
    inc_pc()


def st(op):
    dd, ss = ddss(op)
    print('ST  ', dd, ss)
    inc_pc()


def add(op):
    dd, ss = ddss(op)
    print('ADD ', dd, ss)
    inc_pc()


def adc(op):
    dd, ss = ddss(op)
    print('ADC ', dd, ss)
    inc_pc()


def sub(op):
    dd, ss = ddss(op)
    print('SUB ', dd, ss)
    inc_pc()


def sbb(op):
    dd, ss = ddss(op)
    print('SBB ', dd, ss)
    inc_pc()


def or_(op):
    dd, ss = ddss(op)
    print('OR  ', dd, ss)
    inc_pc()


def xor(op):
    dd, ss = ddss(op)
    print('XOR ', dd, ss)
    inc_pc()


def and_(op):
    dd, ss = ddss(op)
    print('AND ', dd, ss)
    inc_pc()


def cmp(op):
    dd, ss = ddss(op)
    print('CMP ', dd, ss)
    inc_pc()


if __name__ == '__main__':
    load_program('fibo.bin')
    run(0)
