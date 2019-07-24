from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    out('>')
    label('loop')
    label('in1')
    jpi('in1')
    in_(A)
    label('out1')
    jpo('out1')
    out(A)
    jmp('loop')

    end(__file__)

