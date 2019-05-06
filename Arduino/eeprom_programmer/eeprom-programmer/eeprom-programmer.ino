#define SHIFT_DATA 2
#define SHIFT_CLK 3
#define SHIFT_LATCH 4
#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_EN 13

void setAddress(int address, bool outputEnable) {
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, (address >> 8) | (outputEnable ? 0x00 : 0x80));
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, address);

  digitalWrite(SHIFT_LATCH, LOW);
  delayMicroseconds(1);
  digitalWrite(SHIFT_LATCH, HIGH);
  delayMicroseconds(1);
  digitalWrite(SHIFT_LATCH, LOW);
  delay(1);
}

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

void writeEEPROM(int address, byte data) {
  setAddress(address, /*outputEnable*/ false);
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, OUTPUT);
  }

  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  delay(10);
  digitalWrite(WRITE_EN, LOW);
  delayMicroseconds(1);
  digitalWrite(WRITE_EN, HIGH);
  delay(10);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);
  Serial.begin(57600);
}

// Read a line of data from the serial connection.
char * readLine(char * buffer, int len)
{
    for (int ix = 0; (ix < len); ix++)
    {
         buffer[ix] = 0;
    }

    // read serial data until linebreak or buffer is full
    char c = ' ';
    int ix = 0;
    do {
        if (Serial.available())
        {
            c = Serial.read();
            if ((c == '\b') && (ix > 0))
            {
                // Backspace, forget last character
                --ix;
            }
            buffer[ix++] = c;
//            Serial.write(c);
        }
    } while ((c != '\n') && (ix < len));

    buffer[ix - 1] = 0;
    return buffer;
}

void printContents(uint32_t start, uint32_t leng) {
  for (int base = start; base < start+leng; base += 16) {
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
  
void read_rom(char *operand) {
  uint32_t address = convertHex(operand);
  Serial.print("Reading from address ");
  Serial.println(address, HEX);
  printContents(address, 16);
}

void save_rom(char* operand) {
  char line[256];
  uint32_t address = convertHex(operand);
  Serial.print("Saving to address ");
  Serial.println(address, HEX);
  uint32_t count = 0;
  for(;;count++) {
    readLine(line, sizeof(line));
    Serial.println(line);
    if (line[0] == '.') break;
    byte data = (byte)convertHex(line);
    writeEEPROM(address+count, data);
    Serial.print(data,HEX);
    Serial.print(" written to ");
    Serial.println(address+count,HEX);
  }
  Serial.print(count-1, HEX);
  Serial.print(" bytes writen to address ");
  Serial.print(address);
}

uint32_t convertHex(char *text) {
  uint32_t num = 0;
  for(int i=0; text[i]!='\0' && i<255; i++) {
    char c = text[i];
    byte n = c - '0';
    if (c>='A' && c<='F') n = c - 'A' + 10; 
    if (c>='a' && c<='F') n = c - 'a' + 10; 
    num = (num<<4)|n;
  }
  return num;
}

boolean do_command(char command[]) {
  char comm = command[0];
  if (comm == 'R') {
    read_rom(command+1);
  } else if (comm == 'S') {
    save_rom(command+1);
  } else if (comm == 'X') {
    return true;
  } else if (comm == 'G') {
    Serial.println("GO");
  }
  return false;
}

void loop() {

    word w;
    char line[256];
    char *input;
    uint32_t numBytes;
    boolean halt = false;

    input = readLine(line, sizeof(line));
    Serial.println(input);
    halt = do_command(line);
    if (halt) {
      Serial.print("Halting\n");
      delay(1000);
      exit(0);
    }
}
