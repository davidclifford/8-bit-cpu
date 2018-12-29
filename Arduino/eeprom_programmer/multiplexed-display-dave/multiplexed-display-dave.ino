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

#define D0 0x0
#define D1 0x100
#define D2 0x200
#define D3 0x300
#define NEGATIVE 0x400
#define HEXA 0x800
#define OCTAL 0xc00
#define ALPHA 0x1000

#define BLANK 0x0
#define NEG 0x1
#define LTR_H 0x37
#define LTR_O 0x1d

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
  for (int base = 0; base < 8195; base += 16) {
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

int digit(int value, int place, int div) {
  byte digits[] = { 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b }; // with 0 for zero

  int p = place & 0x3FF;
  int digit = digits[abs(value/div)%10];
  if(value>=0) {
    if(value<10 && p==D1) digit = BLANK;
    if(value<100 && p==D2) digit = BLANK;
    if(p==D3) digit = BLANK;
  } else {
    if(abs(value)<10 && p==D1) digit = (value<0) ? NEG : BLANK;
    if(abs(value)<100 && p==D2) digit = (value<=-10) ? NEG : BLANK;
    if(p==D3) digit = (value<=-100) ? NEG : BLANK; 
  }
  return digit;
}

void setup() {
  // put your setup code here, to run once:
  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);
  Serial.begin(57600);

  Serial.println("Programming unsigned numbers");
  for (int value = 0; value <= 255; value += 1) {
    writeEEPROM((byte)value | D0, digit(value, D0, 1));
    writeEEPROM((byte)value | D1, digit(value, D1, 10));
    writeEEPROM((byte)value | D2, digit(value, D2, 100));
    writeEEPROM((byte)value | D3, digit(value, D3, 1));
    if(value%16==0) Serial.print(".");
  }
  Serial.println();
  
  Serial.println("Programming signed numbers");
  for (int value = -128; value <= 127; value += 1) {
    writeEEPROM((byte)value | NEGATIVE | D0, digit(value, D0, 1));
    writeEEPROM((byte)value | NEGATIVE | D1, digit(value, D1, 10));
    writeEEPROM((byte)value | NEGATIVE | D2, digit(value, D2, 100));
    writeEEPROM((byte)value | NEGATIVE | D3, digit(value, D3, 1));
    if(value%16==0) Serial.print(".");
  }
  Serial.println();

  //byte hex[] = { 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b, 0x7d, 0x1f, 0x0d, 0x3d, 0x6f, 0x47 }; //lowercase
  byte hex[] = { 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b, 0x77, 0x1f, 0x4e, 0x3d, 0x4f, 0x47 }; // uppercase
  Serial.println("Programming hex numbers");
  for (int value = 0; value <= 255; value += 1) {
    writeEEPROM((byte)value | HEXA | D0, hex[(value%16)]);
    writeEEPROM((byte)value | HEXA | D1, hex[((value/16)%16)]);
    writeEEPROM((byte)value | HEXA | D2, BLANK);
    writeEEPROM((byte)value | HEXA | D3, LTR_H);
    if(value%16==0) Serial.print(".");
  }
  Serial.println();

  byte digits[] = { 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70}; // 0-7
  Serial.println("Programming octal numbers");
  for (int value = 0; value <= 255; value += 1) {
    writeEEPROM((byte)value | OCTAL | D0, digits[(value%8)]);
    writeEEPROM((byte)value | OCTAL | D1, digits[((value/8)%8)]);
    writeEEPROM((byte)value | OCTAL | D2, digits[((value/64)%8)]);
    writeEEPROM((byte)value | OCTAL | D3, LTR_O);
    if(value%16==0) Serial.print(".");
  }
  Serial.println();

  byte letters[] = { BLANK, 0x7d, 0x1f, 0x0d, 0x3d, 0x6f, 0x47, 0x7b, //space, a-g
                      0x17, 0x50, 0x58, 0x37, 0x0e, 0x4f, 0x15, 0x1d, // h-o
                      0x67, 0x73, 0x05, 0x19, 0x0f, 0x1c, 0x0c, 0x79, // p-w
                      0x37, 0x3b, 0x25, 0x80, 0xb0, 0xe5, 0x08, 0x01}; //x-z, . ! ? _ - 
  Serial.println("Programming alpha");
  for (int disp = 0; disp<4; disp++) {
    for (int value = 0; value <= 32; value += 1) {
      int let1 = BLANK;
      int let2 = BLANK;
      int let3 = BLANK;
      int let4 = BLANK;
      if (disp==0) let1 = letters[value];
      if (disp==1) let2 = letters[value];
      if (disp==2) let3 = letters[value];
      if (disp==3) let4 = letters[value];
      writeEEPROM((byte)value+disp*32 | ALPHA | D3, let1); 
      writeEEPROM((byte)value+disp*32 | ALPHA | D2, let2); 
      writeEEPROM((byte)value+disp*32 | ALPHA | D1, let3); 
      writeEEPROM((byte)value+disp*32 | ALPHA | D0, let4); 
      if(value%16==0) Serial.print(".");
    }
  }
  Serial.println();
  // Read and print out the contents of the EERPROM
  Serial.println("Reading EEPROM");
  printContents();
}

void loop() {
  // put your main code here, to run repeatedly:

}
