# David's 8-bit-cpu

Inspired by the Ben Eater series of videos on youtube https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU
Also see James Bates videos https://www.youtube.com/watch?v=gqYFT6iecHw&list=PL_i7PfWMNYobSPpg1_voiDe6qBcjvuVui

Improvements and thoughts making my own:

Even though Ben Eaters CPU is 8-bit it uses only 4 bits for the address
giving it only 16 locations for instructions and/or data.

The most obvious improvement is to use an 8 bit address giving 256 locations for instructions or data.
However this also means that programming the CPU with DIP switches can be tedious and error prone.
This can be overcome by using a ROM to store the program instead.

Adding more ROMS in the control unit also makes the CPU more powerful as there are more control lines.

For my CPU I used:

4 ROMS for the control signals (28C64)
4 general purpose data registers
A stack pointer
2 74161 counters for the PC
2 74382 chips for the ALU

Having write only registers for the inputs to the ALU (called X&Y)
A mux from the bus to the X & Y registers that reverse the bits (more on this later)
A mux as a zero input to the ALU Y input (used for inc and dec instructions)
Connecting the Instruction Register input straight from the Memory, bypassing the data bus,
  which makes the fetch cycle only need 1 t-state instead of 2
Making my own ROM programmer with a nano Arduino and programming ROMS from a PC
Using a nano as an input/output

Tips:
Use the best quality breadboards you can afford. I started with Elegoo breadboards and regretted it.
I ended up buying BPS BB830 breadboards, the ones Ben Eater recommended, and had little problems from then on.
