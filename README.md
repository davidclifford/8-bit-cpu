# David's 8-bit-cpu

Inspired by the Ben Eater series of videos on youtube https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU

Also see James Bates videos https://www.youtube.com/watch?v=gqYFT6iecHw&list=PL_i7PfWMNYobSPpg1_voiDe6qBcjvuVui

## Improvements and thoughts

Even though Ben Eaters CPU is 8-bit it uses only 4 bits for the address giving it only 16 locations for instructions and/or data.

The most obvious improvement is to use an 8 bit address giving 256 locations for instructions or data.
However this also means that programming the CPU with DIP switches can be tedious and error prone.
This can be overcome by using a ROM to store the program instead.
The control unit was extended by adding two more ROMS to make the CPU more powerful with 32 control lines.

## For my CPU I used

- 4 ROMS for the control signals (28C64) giving 32 control lines
- 4 general purpose data registers (A,B,C,D)
- An 8-bit stack pointer (SP)
- 2 74161 counters for the PC
- 2 74382 chips for the ALU giving AND, OR and XOR as well as ADD and SUB
- Having write only registers for the inputs to the ALU (X,Y)
- A mux from the bus to the X & Y registers that reverse the bits for right shifts
- A mux as a zero input to the ALU Y input so that the ALU can add 1, 0 or -1 to X depending on the ALU function and carry in
- Connecting the Instruction Register input straight from the Memory, bypassing the data bus, which makes the fetch cycle only need 1 t-state instead of 2
- Using a nano as an input/output device
- Using a 28C64 ROM for the multiplexed 4 digit display giving signed & unsigned decimal, octal, hex and a simple ascii display 

## Software & hardware tools

- Using a MiniPro ROM burner to program the ROMs from a PC as this is more powerful than using an Arduino programmer
- Python to generate the control and digital display ROMS
- Python assembler and emulator

## Why use X and Y write only registers in the ALU?

I reasoned that if I had 2 dedicated registers for the inputs to the ALU it would leave
the other registers free to do whatever they needed. It also allowed other registers
like the PC and Stack Pointer to use the ALU without affecting the general purpose registers.
They do need 2 extra control lines and complicate the ALU some more but makes it far more flexible.

## Right shifts

The technique I use is very unorthodox. I knew that left shifts were relatively easy, just add a number to itself.
This also means that I could use carry in to shift bits in and carry out to shift bits out and zero detect
came for free. So I reasoned that right shifts are the same as left shifts but in the opposite direction, so why not
just reverse the bits of the X & Y registers before adding them together and then reversing the bits on
the output. This worked but added a few more chips to the ALU. I've never heard of anyone doing this before.

# Other instructions

- HALT: in Ben Eaters CPU the HALT instruction stopped the clock with a control line but you can remove
that by getting the HALT instruction to decrement the PC via the ALU, so that it will produce
an infinite loop in the micro-code

## Build Tips

Use the best quality breadboards you can afford. I started with Elegoo breadboards and they were terrible.
So I ended up buying BPS BB830 breadboards, the ones Ben Eater recommended, and had very little problems from then on.

![Test Image 1](3DTest.png)