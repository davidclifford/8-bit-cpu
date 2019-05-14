from Python.assembler.asm import *
if __name__ == '__main__':

    # while True:
    #     a = 1
    #     b = 0
    #     while True:
    #         a = a + b
    #         if a > 255:
    #             break
    #         print(a)
    #         b = a - b

    begin()

    label('start')

    mov(A, 0)
    mov(B, 1)

    label('next')
    add(A, B)
    jpc('start')
    out(A)
    sub(B, A)
    jmp('next')

    end('fibo2')


