#################
# THE ASSEMBLER #
#################
import os

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

LDM = 0xD8
LDA = 0xDC

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

address = 0
labels = dict()
todo_labels = dict()
start = None
last = 0

A = '_A_'
B = '_B_'
C = '_C_'
D = '_D_'

regs = [A, B, C, D]

program = [None for _ in range(256)]


def rr(reg):
    code = 0
    if reg == A:
        code = 0
    elif reg == B:
        code = 1
    elif reg == C:
        code = 2
    elif reg == D:
        code = 3
    return code


def ddss(reg1, reg2):
    return rr(reg1)*4 + rr(reg2)


def begin():
    print()
    org(0)


def inc_addr():
    global address, last
    address += 1
    if address > last:
        last = address


def org(_address):
    global address, start
    address = _address
    if start is None or _address < start:
        start = _address


def label(_label):
    global address, program
    labels[_label] = address
    if _label in todo_labels:
        addr_list = todo_labels[_label]
        for addr in addr_list:
            program[addr] = address
        todo_labels.pop(_label)


def get_label(addr):
    global program, address, labels, todo_labels
    if addr in labels:
        return labels[addr]
    else:
        if addr not in todo_labels:
            todo_labels[addr] = []
        todo_labels[addr].append(address)
    return 0


def var(_label):
    global address
    label(_label)
    inc_addr()


def equ(_label, num):
    global labels
    labels[_label] = num


def binary(instr, reg, op):
    global address, program
    num = op
    if isinstance(op, str) and op in regs:
        program[address] = instr + ddss(reg, op)
        inc_addr()
        return
    program[address] = instr + ddss(reg, reg)
    inc_addr()
    if isinstance(op, str):
        num = get_label(op)
    program[address] = num
    inc_addr()


def unary(instr, reg):
    global address, program
    if isinstance(reg, str):
        program[address] = instr + rr(reg)
    else:
        program[address] = instr + reg
    inc_addr()


def single(instr):
    global address, program
    program[address] = instr
    inc_addr()


def jump(instr, addr):
    global address, program
    program[address] = instr
    inc_addr()
    if isinstance(addr, str):
        program[address] = get_label(addr)
    else:
        program[address] = addr
    inc_addr()


def save_bin(filename):
    print("\nSaving {:s} as binary file".format(filename))
    rom0 = bytearray()
    for i in range(256):
        rom0.append(program[i] or 0)
    rombin = open(filename, "wb")
    rombin.write(rom0)
    rombin.close()


################
# INSTRUCTIONS #
################

def hlt():
    single(HLT)


def sp(op):
    jump(SP, op)


def call(op):
    jump(CALL, op)


def ret():
    single(RET)


def calr(reg):
    unary(CALR, reg)


def push(reg):
    unary(PUSH, reg)


def pop(reg):
    unary(POP, reg)


def mov(reg, op):
    binary(MOV, reg, op)


def ld(reg, op):
    binary(LD, reg, op)


def st(reg, op):
    binary(ST, reg, op)


def add(reg, op):
    binary(ADD, reg, op)


def adc(reg, op):
    binary(ADC, reg, op)


def sub(reg, op):
    binary(SUB, reg, op)


def sbb(reg, op):
    binary(SBB, reg, op)


def and_(reg, op):
    binary(AND, reg, op)


def or_(reg, op):
    binary(OR, reg, op)


def xor(reg, op):
    binary(XOR, reg, op)


def cmp(reg, op):
    binary(CMP, reg, op)


def in_(reg):
    unary(IN, reg)


def out(reg):
    unary(OUT, reg)


def not_(reg):
    unary(NOT, reg)


def inc(reg):
    unary(INC, reg)


def dec(reg):
    unary(DEC, reg)


def lsr(reg):
    unary(LSR, reg)


def lsl(reg):
    unary(LSL, reg)


def rol(reg):
    unary(ROL, reg)


def ror(reg):
    unary(ROR, reg)


def jmp(addr):
    jump(JMP, addr)


def jpc(addr):
    jump(JPC, addr)


def jpn(addr):
    jump(JPN, addr)


def jpv(addr):
    jump(JPV, addr)


def jpz(addr):
    jump(JPZ, addr)


def jpr(reg):
    unary(JPR, reg)


def nop():
    single(NOP)


def ldm(reg):
    jump(LDM, reg)


def lda(reg):
    unary(LDA, reg)


def end(filename):
    global program, start, last
    skip = True
    for i in range(start, last):
        line = program[i]
        if line is not None:
            print("{:02X} {:02X}".format(i, line))
            skip = True
        elif skip:
            print('**')
            skip = False

    save_bin(filename+'.bin')
