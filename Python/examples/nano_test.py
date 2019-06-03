from Python.assembler.asm import *
import os
if __name__ == '__main__':
    begin()

    nop()
    label('start')
    in_(A)
    out(A)
    jmp('start')
    # mov(B, 'name')
    # label('loop')
    # lda(B)
    # cmp(A, 0)
    # jpz('start')
    # out(A)
    # inc(B)
    # jmp('loop')
    #
    # org(0x20)
    # var('name', 'Hello, World\r\n')

    end(os.path.dirname(__file__)+'/nano_test')


