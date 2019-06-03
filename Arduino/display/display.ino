#define D0 2 
#define D1 3 
#define D2 4 
#define D3 5 
#define D4 6 
#define D5 7 
#define D6 8 
#define D7 9

#define IN 10
#define OUT 11
#define ADR 12
#define CLK 13

void setup() {
  Serial.begin(115200);
  set_input(CLK);
}

int _clk;
int clk;
bool adr;
bool in;
bool out;
bool up_edge;
bool dn_edge;
int address = 0;

void loop() {
  // put your main code here, to run repeatedly:
  _clk = clk;
  clk = digitalRead(CLK);
  in = (digitalRead(IN)==0);
  out = (digitalRead(OUT)==0);
  adr = (digitalRead(ADR)==0);

  up_edge = (_clk == 0 && clk == 1);
  dn_edge = (_clk == 1 && clk == 0);
  if (dn_edge && out) {
    Serial.print((char)get_data());
  }
  if (dn_edge && in) {
    byte data = 0;
    if (Serial.available() > 0)
      data = (byte)Serial.read();
    set_data(data);    
  }
  if (dn_edge && adr) {
    address = get_data();
  }  
}

byte get_data() {
    byte data = 0;
    for (int pin = D0; pin <= D7; pin += 1) {
      data = (data << 1) + digitalRead(pin);
    }
    return data;
}

void set_data(byte data) {
  set_output();
  for (int pin = D7; pin >= D0; pin -= 1) {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  while(digitalRead(IN)==0)
    delayMicroseconds(1);
  set_input(D7);
}

void set_input(int last) {
  for (int i=D0; i<=last; i++) {
      pinMode(i, INPUT);
  }
}

void set_output() {
  for (int i=D0; i<=D7; i++) {
      pinMode(i, OUTPUT);
  }
}
