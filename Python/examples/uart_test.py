from Python.assembler.asm import *
if __name__ == '__main__':
    begin()

    nop()
    out('>')
    label('start')
    mov(B, 'phrase')
    label('loop')
    lda(B)
    # in_(A)
    cmp(A, 0)
    jpz('start')
    label('out1')
    jpo('out1')
    out(A)
    inc(B)
    jmp('loop')

    org(0x80)
    var('phrase', 'The quick brown fox jumps over the lazy dog!', 10, 13, 0)

    end(__file__)

