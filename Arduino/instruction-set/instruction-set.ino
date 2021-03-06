#define ROM 0

//#define CLEARROM 1
//#define FILLNOP 1
//#define TESTINSTR 1
#define RAW
//#define CONTENTS 1
//#define INSTRUCTIONS 1
//#define CONTROL 1


#define SHIFT_DATA 2
#define SHIFT_CLK 3
#define SHIFT_LATCH 4
#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_EN 13

#define DOT "."

#define IL ((uint32_t)1<< 0) // Instruction reg load
#define RO ((uint32_t)1<< 1) // Ram out
#define XI ((uint32_t)1<< 2) // ALU X in
#define YI ((uint32_t)1<< 3) // ALU Y in
#define EO ((uint32_t)1<< 4) // ALU result out
#define MI ((uint32_t)1<< 5) // Mem address in
#define PC ((uint32_t)1<< 6) // Prog count increment
#define PO ((uint32_t)1<< 7) // Prog counter out

#define AI ((uint32_t)1<< 8) // A reg in
#define AO ((uint32_t)1<< 9) // A reg out
#define BI ((uint32_t)1<<10) // B reg in
#define BO ((uint32_t)1<<11) // B reg out
#define RI ((uint32_t)1<<12) // Ram in
#define JP ((uint32_t)1<<13) // Jump (PC in)
#define OI ((uint32_t)1<<14) // Output in (display)
#define TR ((uint32_t)1<<15) // Reset T states

#define S0 ((uint32_t)1<<16) // ALU setting 0
#define S1 ((uint32_t)1<<17) // ALU setting 1
#define S2 ((uint32_t)1<<18) // ALU setting 2
#define CY ((uint32_t)1<<19) // ALU Carry in
#define Y0 ((uint32_t)1<<20) // ALU Y zero
#define RV ((uint32_t)1<<21) // ALU Reverse bits into X&Y
#define FL ((uint32_t)1<<22) // ALU Load flags reg from ALU
#define HL ((uint32_t)1<<23) // Halt CPU (not needed?)

#define CI ((uint32_t)1<<24) // C reg in
#define CO ((uint32_t)1<<25) // C reg out
#define DI ((uint32_t)1<<26) // D reg in
#define DO ((uint32_t)1<<27) // D reg out
#define SI ((uint32_t)1<<28) // Stack Pointer in
#define SO ((uint32_t)1<<29) // Stack Pointer out
#define IO ((uint32_t)1<<30) // Input from nano
#define MO ((uint32_t)1<<31) // Memory out from ROM

uint32_t inline flip_bits(uint32_t instruction) {
  instruction ^= (IL|RO|XI|YI|EO|MI|PO| AI|AO|BI|BO|JP|OI|TR| FL| CI|CO|DI|DO|SI|SO|IO|MO);
  return instruction;
}

void writeEEPROM(int address, uint32_t instruction) {
  writeROM(address, 0xFF&(flip_bits(instruction)>>(ROM*8)));
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
void writeROM(int address, byte data) {
  setAddress(address, /*outputEnable*/ false);
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, OUTPUT);
  }

  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  digitalWrite(WRITE_EN, LOW);
  delayMicroseconds(5);
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
      data[offset] = flip_bits((uint32_t)readEEPROM(base + offset)<<(ROM*8))>>(ROM*8);
    }

    char buf[80];
    sprintf(buf, "%03x:  %02x %02x %02x %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x %02x %02x %02x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);

    Serial.println(buf);
  }
}

void printRaw() {
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

void printContentsHex() {
  for (int base = 0; base < 256; base++) {
    byte data[8];
    for (int T = 0; T<8; T++) {
      data[T] = flip_bits((uint32_t)readEEPROM(base<<5|T<<2)<<(ROM*8))>>(ROM*8);
    }

    char buf[80];
    sprintf(buf, "%02x:  %02x %02x %02x %02x %02x %02x %02x %02x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]);

    Serial.println(buf);
  }
}

void printContentsString() {
  uint32_t part = 0;
  for (int base = 0; base < 256; base++) {
    Serial.print(base,HEX);Serial.print(" ");
    for (int T = 0; T<8; T++) {
      part = (0xFF & flip_bits((uint32_t)readEEPROM(base<<5|T<<2)<<(ROM*8))>>(ROM*8))<<(ROM*8);
      printControl(part);
      Serial.print(", ");
    }
    Serial.println();
  }
}

void printControl(uint32_t part) {
  String c = "";
//  Serial.println(part,HEX);
//  Serial.println(part&IL,HEX);
  if (part&IL) c += "IL|";
  if (part&RO) c += "RO|";
  if (part&XI) c += "XI|";
  if (part&YI) c += "YI|";
  if (part&EO) c += "EO|";
  if (part&MI) c += "MI|";
  if (part&PC) c += "PC|";
  if (part&PO) c += "PO|";

  if (part&AI) c += "AI|";
  if (part&AO) c += "AO|";
  if (part&BI) c += "BI|";
  if (part&BO) c += "BO|";
  if (part&RI) c += "RI|";
  if (part&JP) c += "JP|";
  if (part&OI) c += "OI|";
  if (part&TR) c += "TR|";

  if (part&S0) c += "S0|";
  if (part&S1) c += "S1|";
  if (part&S2) c += "S2|";
  if (part&CY) c += "CY|";
  if (part&Y0) c += "Y0|";
  if (part&RV) c += "RV|";
  if (part&FL) c += "FL|";
  if (part&HL) c += "HL|";

  if (part&CI) c += "CI|";
  if (part&CO) c += "CO|";
  if (part&DI) c += "DI|";
  if (part&DO) c += "DO|";
  if (part&SI) c += "SI|";
  if (part&SO) c += "SO|";
  if (part&IO) c += "IO|";
  if (part&MO) c += "MO|";

  Serial.print(c);
  Serial.print(" ");
}

void setup() {
  // put your setup code here, to run once:
  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);
  Serial.begin(57600);

  #define FETCH PO|MI|IL|PC
  #define OPERAND PO|MI|PC
  #define CLEAR 0
  #define BSUB S0
  #define SUB S1
  #define ADD S0|S1
  #define XOR S2
  #define OR S2|S0
  #define AND S2|S1
  #define PRESET S2|S1|S0

#ifdef CLEARROM
  Serial.print(F("Clearing EEPROM "));
  Serial.println(ROM);
  for (int addr = 0; addr < 8192; addr++) {
    writeEEPROM(addr ,0);
    if(addr%32==0) Serial.print(ins>>5,HEX);Serial.print(" ");
  }
  Serial.println();
#endif   
 
  Serial.print(F("Programming EEPROM number "));
  Serial.println(ROM);
  
  const uint32_t inst[][8] PROGMEM = {
                        {FETCH, TR, 0, 0, 0, 0, 0, 0},                           // NOP      00
                        {FETCH, OPERAND, RO|MI, RO|AI|TR, 0, 0, 0, 0},           // LD A,(#) 01
                        {FETCH, OPERAND, RO|MI, RO|BI|TR, 0, 0, 0, 0},           // LD B,(#) 02        
                        {FETCH, OPERAND, RO|MI, AO|RI|TR, 0, 0, 0, 0},           // ST A,(#) 03    
                        {FETCH, OPERAND, RO|MI, BO|RI|TR, 0, 0, 0, 0},           // ST B,(#) 04        
                        {FETCH, OPERAND, RO|AI|TR, 0, 0, 0, 0, 0},               // MOV A,#  05
                        {FETCH, OPERAND, RO|BI|TR, 0, 0, 0, 0, 0},               // MOV B,#  06
                        {FETCH, AI|BO|TR, 0, 0 ,0, 0, 0},                        // MOV A,B  07
                        {FETCH, BI|AO|TR, 0, 0 ,0, 0, 0},                        // MOV B,A  08
                        {FETCH, AO|XI, BO|YI, ADD|EO|AI|FL|TR, 0, 0, 0, 0},      // ADD A,B  09
                        {FETCH, AO|XI, BO|YI, SUB|CY|EO|AI|FL|TR, 0, 0, 0, 0},   // SUB A,B  0A
                        {FETCH, AO|XI, BO|YI, SUB|CY|EO|FL|TR, 0, 0, 0, 0},      // CMP A,B  0B
                        {FETCH, AO|OI|TR, 0, 0, 0, 0, 0, 0},                     // OUT A 0C
                        {FETCH, OPERAND, RO|OI|TR, 0, 0, 0, 0, 0},               // OUT # 0D               
                        {FETCH, OPERAND, RO|JP|TR, 0, 0, 0, 0, 0},               // JP #addr 0E            
                        {FETCH, AO|XI, OPERAND, RO|YI, ADD|EO|AI|TR, 0, 0, 0},   // ADD A,#  0F
                        {FETCH, AO|XI, OPERAND, RO|YI, SUB|CY|EO|AI|TR, 0, 0, 0},// SUB A,#  10
                        {FETCH, AO|XI, Y0|ADD|CY|EO|AI|TR, 0, 0, 0, 0, 0},       // INC A  11
                        {FETCH, AO|XI, Y0|SUB|EO|AI|TR, 0, 0, 0, 0, 0},          // DEC A  12
                        {FETCH, HL, 0, 0, 0, 0, 0, 0},                           // HALT   13
    };

  #ifdef FILLNOP
  Serial.println(F("Fill with NOP"));
  for (int ins = 0; ins < 256; ins ++) {
    if(ins%16==0) Serial.println();
    Serial.print(ins,HEX);Serial.print(" ");
    for(int T=0; T<8; T++) {
      for(int flags = 0; flags<4; flags++) {
        int addr = flags | T<<2 | ins<<5;
        writeEEPROM(addr ,inst[0][T]);
      }
    }
  }
  Serial.println();
  #endif

  #ifdef TESTINSTR
  Serial.print(F("Test instructions"));
  for (int ins = 0; ins < 20; ins++) {
    if(ins%16==0) Serial.println();
    Serial.print(ins,HEX);Serial.print(" ");
    for (int T = 0; T<8; T++) {
      for (int flags = 0; flags<4; flags++) {
        int addr = flags | T<<2 | ins<<5;
        writeEEPROM(addr ,inst[ins][T]);
      }
    }
  } 
  Serial.println();
  #endif

  #ifdef CONTENTS
  // Read and print out the contents of the EERPROM
  Serial.println(F("Reading EEPROM"));
  printContents();
  #endif
  #ifdef RAW
  // Read and print out the contents of the EERPROM
  Serial.println(F("Reading Raw"));
  printRaw();
  #endif  
  #ifdef INSTRUCTIONS
  Serial.println(F("Reading Instructions")); 
  printContentsHex();
  #endif
  #ifdef CONTROL
  Serial.println(F("Reading Control")); 
  printContentsString();
  #endif

  Serial.println(F("Finished"));
}

void loop() {
  // put your main code here, to run repeatedly:

}
