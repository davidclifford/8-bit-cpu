#################
# THE ASSEMBLER #
#################
import os

NOP = 0x00
SP = 0x01
CALL = 0x02
RET = 0x03

OUTI = 0x04
HLT = 0x05
# 0x06
# 0x07
PUSH = 0x08
POP = 0x0C

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

NOT = 0xC0  # to be replaced?
NEG = 0xC4  # to be replaced?
INC = 0xC8  # to be replaced?
DEC = 0xCC  # to be replaced?

IN = 0xD0
OUT = 0xD4

LDM = 0xD8  # Load from ROM memory into register rr e.g. LDM rr,(#addr)
LDA = 0xDC  # Load A reg from ROM memory addressed by a register e.g. LDA (rr)

LSL = 0xE0
LSR = 0xE4
ROL = 0xE8  # to be replaced?
ROR = 0xEC  # to be replaced?

# 3 bits for selecting C,Z,N,V,I,O
JPC = 0xF0
JPZ = 0xF1
JPN = 0xF2
JPV = 0xF3
JPI = 0xF4
JPO = 0xF5

# ??? = 0xF6
# ??? = 0xF7

JNC = 0xF8
JNZ = 0xF9
JNN = 0xFA
JNV = 0xFB
JNI = 0xFC
JNO = 0xFD

# ??? = 0xFE

JMP = 0xFF


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

PROGRAM_SPACE = 256
program = [None for _ in range(512)]


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


def var(_label, *vals):
    global address, program
    label(_label)
    for val in vals:
        if isinstance(val, str):
            for c in val:
                data(ord(c))
            # data(0)
        else:
            data(val)


def equ(_label, num):
    global labels
    labels[_label] = num


def prog(instruct):
    global address, program
    program[address + PROGRAM_SPACE] = instruct
    inc_addr()


def operand(instruct):
    global address, program
    program[address % 256] = instruct


def data(instruct):
    global address, program
    program[address % 256] = instruct
    inc_addr()


def binary(instr, reg, op):
    global address, program
    num = op
    if isinstance(op, str) and op in regs:
        prog(instr + ddss(reg, op))
        return
    prog(instr + ddss(reg, reg))
    if isinstance(op, str):
        num = get_label(op)
    operand(num)


def unary(instr, reg):
    global address, program
    if isinstance(reg, str):
        prog(instr + rr(reg))
    else:
        prog(instr + reg)


def single(instr):
    global address, program
    prog(instr)


def jump(instr, addr):
    global address, program
    prog(instr)
    if isinstance(addr, str):
        operand(get_label(addr))
    else:
        operand(addr)


def save_bin(filename):
    print("\nSaving {:s} as binary file".format(filename))
    rom0 = bytearray()
    for i in range(512):
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


def out(op):
    if isinstance(op, str) and op in regs:
        unary(OUT, op)  # e.g. out(A)
    else:
        if isinstance(op, str) and op:
            jump(OUTI, ord(op[0]))  # e.g. out('A')
        else:
            jump(OUTI, op)  # e.g. out(13)


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


def jnc(addr):
    jump(JNC, addr)


def jnn(addr):
    jump(JNN, addr)


def jnv(addr):
    jump(JNV, addr)


def jnz(addr):
    jump(JNZ, addr)


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
    for i in range(0, 256):
        instr = program[i+PROGRAM_SPACE]
        oper = program[(i+1) % 256]
        if instr is not None:
            if oper is not None:
                print("{:02X} {:02X} {:02X}".format(i, instr, oper))
            else:
                print("{:02X} {:02X}".format(i, instr))
            skip = True
        elif oper is not None:
            print("{:02X} ** {:02X}".format(i+1, oper))
            skip = True
        elif skip:
            print('**')
            skip = False


    print(filename)
    file = os.path.dirname(filename) + '/output/' + os.path.basename(filename)
    file = os.path.splitext(file)[0]
    save_bin(file+'.bin')
