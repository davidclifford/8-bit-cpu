from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    sp(0)
    label('start')
    call('alex')
    out('!')
    call('dad')
    out('?')
    jmp('start')
    hlt()

    label('alex')
    out('A')
    out('l')
    out('e')
    out('x')
    out(13)
    out(10)
    ret()
    hlt()
    label('dad')
    out('D')
    out('a')
    out('d')
    out(13)
    out(10)
    ret()

    end(__file__)


