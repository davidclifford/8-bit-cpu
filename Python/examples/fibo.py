from Python.assembler.assembler import *

begin()

label('start')

mov(A, 0)
mov(B, 1)

label('next')
out(A)
st(B, 'temp')
add(B, A)
ld(A, 'temp')

jpc('start')
jmp('next')

org(0x10)
var('temp')

end()
