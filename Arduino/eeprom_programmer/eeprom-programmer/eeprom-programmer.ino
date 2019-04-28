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

String get_input() {
  String command = "";
  while (Serial.available() <= 0) {
    delay(1);
  }
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == 13) break;
    command = command + c;
  }
  return command;
}

void loop() {

    word w;
    char line[80];
    uint32_t numBytes;

    Serial.print("\n>");
    Serial.flush();
    readLine(line, sizeof(line));  
    Serial.print(line);
    Serial.flush();
}
