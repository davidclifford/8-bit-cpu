/**
 * This sketch is specifically for programming the EEPROM used in the 8-bit
 * decimal display decoder described in https://youtu.be/dLh1n2dErzE
 */
#define SHIFT_DATA 2
#define SHIFT_CLK 3
#define SHIFT_LATCH 4
#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_EN 13

#define IL ((uint32_t)1<<0)
#define RO ((uint32_t)1<<1)
#define XI ((uint32_t)1<<2)
#define YI ((uint32_t)1<<3)
#define EO ((uint32_t)1<<4)
#define MI ((uint32_t)1<<5)
#define PC ((uint32_t)1<<6)
#define PO ((uint32_t)1<<7)

#define AI ((uint32_t)1<<8)
#define AO ((uint32_t)1<<9)
#define BI ((uint32_t)1<<10)
#define BO ((uint32_t)1<<11)
#define RI ((uint32_t)1<<12)
#define Y0 ((uint32_t)1<<13)
#define CY ((uint32_t)1<<14)
#define JP ((uint32_t)1<<15)

/*
_PO	PC out			\
 PC	Inc PC			|
_MI	Mem address in	| - Needed for fetch/execute
_IL 	IR load		/
_RO	Ram out		- Get Data for instruction/data
_XI	X in		\
_YI	Y in		| - Arithmetic on 2 numbers & result
_EO	ALU out		/

_AI	Reg A in	\
_AO	Reg A out	| - Load/store/move
_BI	Reg B in	|   between registers
_BO	Reg B out	|	 and memory
_RI	Ram In		/
 Y0	Y=0			\ - Implement Inc
 CY	Carry in	/
_JP	Jump (PC in)  - Unconditional jump
		
 S0	ALU sel \
 S1		"	| - Select ALU function
 S2		"	/
 RV	Reverse bits  - for right shifting
_FL	Flag reg load - conditional jumps
_OI	Output in     - output to display (or UART?)
 PR	Prog	      - Use program memory
_TR	T-state reset - Reset T-state counter for more efficient instruction speed		

_CI	Reg C in	\
_CO	Reg C out	|
_DI	Reg D in	| - C,D, and SP registers
_DO	Reg D out	|
_SI	SP in		|
_SO	SP out		/
_DM	Disp mode in  - Which display mode: dec/signed/octal/hex/dascii
 HL	Halt          - Stop CPU (unneeded?)  
*/
uint32_t inline flip_bits(uint32_t instruction) {
  instruction ^= (IL|RO|XI|EO|MI|PO|AI|AO|BI|BO|RI|JP);
  return instruction;
}

/*
   Output the address bits and outputEnable signal using shift registers.
*/
void setAddress(int address, bool outputEnable) {
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, (address >> 8) | (outputEnable ? 0x00 : 0x80));
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, address);

  digitalWrite(SHIFT_LATCH, LOW);
  digitalWrite(SHIFT_LATCH, HIGH);
  digitalWrite(SHIFT_LATCH, LOW);
}


/*
   Read a byte from the EEPROM at the specified address.
*/
byte readEEPROM(int address) {
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, INPUT);
  }
  setAddress(address, /*outputEnable*/ true);

  byte data = 0;
  for (int pin = EEPROM_D7; pin >= EEPROM_D0; pin -= 1) {
    data = (data << 1) + digitalRead(pin);
  }
  return data;
}


/*
   Write a byte to the EEPROM at the specified address.
*/
void writeEEPROM(int address, byte data) {
  setAddress(address, /*outputEnable*/ false);
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, OUTPUT);
  }

  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  digitalWrite(WRITE_EN, LOW);
  delayMicroseconds(1);
  digitalWrite(WRITE_EN, HIGH);
  delay(10);
}

/*
   Read the contents of the EEPROM and print them to the serial monitor.
*/
void printContents() {
  for (int base = 0; base < 8192; base += 16) {
    byte data[16];
    for (int offset = 0; offset < 16; offset++) {
      data[offset] = readEEPROM(base + offset);
    }

    char buf[80];
    sprintf(buf, "%03x:  %02x %02x %02x %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x %02x %02x %02x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);

    Serial.println(buf);
  }
}

void setup() {
  // put your setup code here, to run once:
  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);
  Serial.begin(57600);

//  Serial.println("Clearing EEPROM");
//  for (int addr = 0; addr < 8192; addr += 1) {
//    writeEEPROM(addr ,flip_bits(0));
//    if(addr%256==0) Serial.print(".");
//  }
//  Serial.println();

  #define FETCH PO|MI|IL|PC
  uint32_t inst[][8] = {
                        {FETCH, 0, 0, 0, 0, 0, 0, 0}, // NOP 00
                        {FETCH, PO|MI|PC, RO|MI, RO|XI, 0, 0, 0, 0}, // LDX addr 01
                        {FETCH, PO|MI|PC, RO|XI, 0, 0, 0, 0, 0}, // LXI # 02
                        {FETCH, PO|MI|PC, RO|MI, RO|YI, 0, 0, 0, 0}, // LDY addr 03
                        {FETCH, PO|MI|PC, RO|YI, 0, 0, 0, 0, 0}, // LYI # 04
                        {FETCH, EO|XI, 0, 0, 0, 0, 0, 0}, // ADD and output 05
                      };
  Serial.println("Fetch micro-instruction");
  for (int addr = 0; addr < 8192; addr += 32) {
    writeEEPROM(addr ,flip_bits(PO|MI|IL|PC));
    if(addr%256==0) Serial.print(".");
  }
  Serial.println();

  Serial.println("Test instructions");
  for (int ins = 0; ins < 6; ins++) {
    for (int T = 0; T<8; T++) {
      for (int flags = 0; flags<4; flags++) {
        int addr = flags | T<<2 | ins<<5;
        writeEEPROM(addr ,flip_bits(inst[ins][T]));
      }
    }
    Serial.print(".");
  } 
  Serial.println();

  // Read and print out the contents of the EERPROM
  Serial.println("Reading EEPROM");
  printContents();
}

void loop() {
  // put your main code here, to run repeatedly:

}
