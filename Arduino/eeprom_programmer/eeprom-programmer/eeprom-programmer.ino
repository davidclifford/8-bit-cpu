void setup() {
  // put your setup code here, to run once:
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
            Serial.write(c);
        }
    } while ((c != '\n') && (ix < len));

    buffer[ix - 1] = 0;
    return buffer;
}

void read_rom() {
  Serial.print("Dumping contents of ROM\n");
}

void save_rom() {
  Serial.print("Saving ROM\n");
}

boolean do_command(char command[]) {
  char comm = command[0];
  if (comm == 'R') {
    read_rom();
  } else if (comm == 'S') {
    save_rom();
  } else if (comm == 'X') {
    return true;
  } else if (comm == 'G') {
    Serial.print("Ready\n");
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
    halt = do_command(line);
    if (halt) {
      Serial.print("Halting\n");
      delay(1000);
      exit(1);
    }
}
