from Python.assembler.assembler import *

begin()

label('start')

mov(A, 0)
mov(B, 1)

label('next')
st(B, 'temp')
add(B, A)
ld(A, 'temp')
out(A)
jpc('start')
jmp('next')

org(0x10)
var('temp')

end()
