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
#define Y0 ((uint32_t)1<<13) // ALU Y zero
#define CY ((uint32_t)1<<14) // ALU Carry in
#define JP ((uint32_t)1<<15) // Jump (PC in)

#define S0 ((uint32_t)1<<16) // ALU setting 0
#define S1 ((uint32_t)1<<17) // ALU setting 1
#define S2 ((uint32_t)1<<18) // ALU setting 2
#define RV ((uint32_t)1<<19) // Reverse bits into X&Y
#define FL ((uint32_t)1<<20) // Load flags reg from ALU
#define OI ((uint32_t)1<<21) // Output in (display)
#define PR ((uint32_t)1<<22) // Use PRogram memory (or ROM?)
#define TR ((uint32_t)1<<23) // Reset T states

#define CI ((uint32_t)1<<24) // C reg in
#define CO ((uint32_t)1<<25) // C reg out
#define DI ((uint32_t)1<<26) // D reg in
#define DO ((uint32_t)1<<27) // D reg out
#define SI ((uint32_t)1<<28) // Stack Pointer in
#define SO ((uint32_t)1<<29) // Stack Pointer out
#define DM ((uint32_t)1<<30) // Display mode in (dec/signed/hex/octal/dascii)
#define HL ((uint32_t)1<<31) // Halt CPU (not needed?)

uint32_t inline flip_bits(uint32_t instruction) {
  instruction ^= (IL|RO|XI|YI|EO|MI|PO| AI|AO|BI|BO|RI|JP| FL|OI|TR| CI|CO|DI|DO|SI|SO|DM);
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

  Serial.println("Clearing EEPROM");
  for (int addr = 0; addr < 8192; addr += 1) {
    writeEEPROM(addr ,flip_bits(0));
    if(addr%256==0) Serial.print(".");
  }
  Serial.println();

  #define FETCH PO|MI|IL|PC
  
  uint32_t inst[][8] = {
                        {FETCH, 0, 0, 0, 0, 0, 0, 0}, // NOP 00
                        {FETCH, PO|MI|PC, RO|XI, 0, 0, 0, 0, 0}, // LXI # 01
                        {FETCH, PO|MI|PC, RO|YI, 0, 0, 0, 0, 0}, // LYI # 02
                        {FETCH, EO|XI, 0, 0, 0, 0, 0, 0}, // ADX (X=X+Y) 03
                        {FETCH, EO|YI, 0, 0, 0, 0, 0, 0}, // ADY (Y=X+Y) 04
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
