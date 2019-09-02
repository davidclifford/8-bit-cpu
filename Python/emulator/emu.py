################
# THE EMULATOR #
################

A = 0
B = 1
C = 2
D = 3
FLAG_CY = 0
FLAG_ZERO = 1
FLAG_NEG = 2
FLAG_OVER = 3
FLAG_IN = 4
FLAG_OUT = 5

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


class Emulator(object):

    SP = 0
    PC = 0
    PROG = [0 for _ in range(512)]
    MEM = [0 for _ in range(256)]
    REGS = [0 for _ in range(4)]
    FLAGS = [0 for _ in range(8)]

    def load_program(self, filename):
        rombin = open(filename, "rb")
        self.PROG = rombin.read(512)
        rombin.close()
        # for i in range(256):
        #     print('{:02X}: {:02X} {:02X}'.format(i, self.PROG[i+256], self.PROG[i]))

    def run(self, address):
        self.PC = address
        while True:
            self.status()
            self.opcode(self.PC)
            print()
            print()

    def opcode(self, address):
        op = self.PROG[address+256]
        self.inc_pc()
        self.perform(op)

    def operand(self):
        oper = self.PROG[self.PC]
        return oper

    def inc_pc(self):
        self.PC += 1
        if self.PC > 255:
            self.PC = 0
            exit(0)

    def jmp_pc(self, pc):
        self.PC = pc

    def result(self, comp, flags=False):
        res = comp
        if flags:
            self.FLAGS[FLAG_CY] = res > 255 or res < 0
        if res > 255:
            res = res - 256
        if res < 0:
            res = res + 256

        if flags:
            self.FLAGS[FLAG_ZERO] = res == 0
            self.FLAGS[FLAG_NEG] = res >= 128

        return res

    def _r(self, ss):
        return self.REGS[ss]

    def _w(self, dd, num):
        self.REGS[dd] = num

    def status(self):
        reg = 'A {:02X} B {:02X} C {:02X} D {:02X} SP {:02X} '.format(self.REGS[A], self.REGS[B],
                                                                      self.REGS[C], self.REGS[D], self.SP)
        flag = 'C' if self.FLAGS[FLAG_CY] else 'c'
        flag = flag + ('Z' if self.FLAGS[FLAG_ZERO] else 'z')
        flag = flag + ('N' if self.FLAGS[FLAG_NEG] else 'n')
        flag = flag + ('V' if self.FLAGS[FLAG_OVER] else 'v')
        pc_flag = 'PC {:02X} {:s}'.format(self.PC, flag)
        print(pc_flag)
        print(reg)

    def print_op(self, op, *args):
        print(op, end='')
        for arg in args:
            if isinstance(arg, int):
                print('{:02X}'.format(arg), end='')
            else:
                print(arg, end='')

    def perform(self, op):
        mask = op & 0xF0
        if mask == 0:
            self.misc(op)
        elif mask == MOV:
            self.move(op)
        elif mask == LD:
            self.ld(op)
        elif mask == ST:
            self.st(op)
        elif mask == ADD:
            self.add(op)
        elif mask == ADC:
            self.adc(op)
        elif mask == SUB:
            self.sub(op)
        elif mask == SBB:
            self.sbb(op)
        elif mask == OR:
            self.or_(op)
        elif mask == XOR:
            self.xor(op)
        elif mask == AND:
            self.and_(op)
        elif mask == CMP:
            self.cmp(op)
        else:
            self.other(op)

    def ddss(self, op):
        return (op & 0x0C) >> 2, op & 0x03

    def rr(self, op):
        return op & 0x03

    def reg(self, rr):
        return ['A,', 'B,', 'C,', 'D,'][rr]

    def misc(self, op):
        if op == NOP:
            self.nop(op)
        elif op == SP:
            addr = self.operand()
            self.print_op('SP {:02X}'.format(addr))
            self.SP = addr
        elif op == CALL:
            self.call()
        elif op == RET:
            self.ret()
        elif op == HLT:
            self.print_op('HLT')
            self.PC = 0
            exit(0)
        else:
            self.print_op('misc {:02X}'.format(op))

    def other(self, op):

        rr = self.rr(op)
        if op >= JPC:
            self.jump(op)
        elif op == INC:
            self.print_op('INC ', self.reg(rr))
            res = self.result(self._r(rr) + 1, True)
            self._w(rr, res)
        elif op == DEC:
            self.print_op('DEC ', self.reg(rr))
            res = self.result(self._r(rr) - 1, True)
            self._w(rr, res)
        else:
            self.print_op('other {:02X}'.format(op))

    def jump(self, op):
        if op == JPC:
            self.print_op('JPC ', self.operand())
            if self.FLAGS[FLAG_CY] == 1:
                self.jmp_pc(self.operand())
        elif op == JPZ:
            self.print_op('JPZ ', self.operand())
            if self.FLAGS[FLAG_ZERO] == 1:
                self.jmp_pc(self.operand())
        elif op == JPN:
            self.print_op('JPN ', self.operand())
            if self.FLAGS[FLAG_NEG] == 1:
                self.jmp_pc(self.operand())
        elif op == JPV:
            self.print_op('JPV ', self.operand())
            if self.FLAGS[FLAG_OVER] == 1:
                self.jmp_pc(self.operand())
        elif op == JPI:
            self.print_op('JPI ', self.operand())
            if self.FLAGS[FLAG_IN] == 1:
                self.jmp_pc(self.operand())
        elif op == JPO:
            self.print_op('JPO ', self.operand())
            if self.FLAGS[FLAG_OUT] == 1:
                self.jmp_pc(self.operand())

        elif op == JPC:
            self.print_op('JNC ', self.operand())
            if self.FLAGS[FLAG_CY] == 0:
                self.jmp_pc(self.operand())
        elif op == JPZ:
            self.print_op('JNZ ', self.operand())
            if self.FLAGS[FLAG_ZERO] == 0:
                self.jmp_pc(self.operand())
        elif op == JPN:
            self.print_op('JNN ', self.operand())
            if self.FLAGS[FLAG_NEG] == 0:
                self.jmp_pc(self.operand())
        elif op == JPV:
            self.print_op('JNV ', self.operand())
            if self.FLAGS[FLAG_OVER] == 0:
                self.jmp_pc(self.operand())
        elif op == JPI:
            self.print_op('JNI ', self.operand())
            if self.FLAGS[FLAG_IN] == 0:
                self.jmp_pc(self.operand())
        elif op == JPO:
            self.print_op('JNO ', self.operand())
            if self.FLAGS[FLAG_OUT] == 0:
                self.jmp_pc(self.operand())
        elif op == JMP:
            self.print_op('JMP ', self.operand())
            self.jmp_pc(self.operand())
        else:
            self.print_op('misc {:02X}'.format(op))

    def nop(self, op):
        self.print_op('NOP')

    def call(self):
        addr = self.operand()
        self.print_op('CALL {:02X}'.format(addr))
        self.dec_sp()
        self.MEM[self.SP] = self.PC
        self.jmp_pc(addr)

    def ret(self):
        self.print_op('RET')
        self.PC = self.MEM[self.SP]
        self.inc_sp()

    def inc_sp(self):
        self.SP += 1
        if self.SP > 255:
            self.SP -= 256

    def dec_sp(self):
        self.SP -= 1
        if self.SP < 0:
            self.SP += 256

    def move(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self._w(dd, num)
            self.print_op('MOV ', self.reg(dd), num)
        else:
            self._w(dd, self._r(ss))
            self.print_op('MOV ', self.reg(dd), self.reg(ss))

    def ld(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self._w(dd, self.MEM[num])
            self.print_op('LD ', self.reg(dd), num)
        else:
            self._w(dd, self.MEM[self._r(ss)])
            self.print_op('LD ', self.reg(dd), self.reg(ss))

    def st(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.MEM[num] = self._r(dd)
            self.print_op('ST ', self.reg(dd), num)
        else:
            address = self._r(dd)
            self.MEM[address] = self._r(ss)
            self.print_op('ST ',self.reg(dd), self.reg(ss))

    def add(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('ADD ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('ADD ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) + num, True)
        self._w(dd, res)

    def adc(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('ADC ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('ADC ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) + num + self.FLAGS[FLAG_CY], True)
        self._w(dd, res)

    def sub(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('SUB ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('SUB ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) - num, True)
        self._w(dd, res)

    def sbb(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('SBB ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('SBB ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) - num + self.FLAGS[FLAG_CY], True)
        self._w(dd, res)

    def or_(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('OR  ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('OR  ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) | num, True)
        self._w(dd, res)

    def xor(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('XOR ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('XOR ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) ^ num, True)
        self._w(dd, res)

    def and_(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('AND ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('AND ', self.reg(dd), self.reg(ss))
        res = self.result(self._r(dd) & num, True)
        self._w(dd, res)

    def cmp(self, op):
        dd, ss = self.ddss(op)
        if dd == ss:
            num = self.operand()
            self.print_op('CMP ', self.reg(dd), num)
        else:
            num = self._r(ss)
            self.print_op('CMP ', self.reg(dd), self.reg(ss))
        self.result(self._r(dd) - num, True)


if __name__ == '__main__':
    emu = Emulator()
    emu.load_program('mult.bin')
    emu.run(0)
