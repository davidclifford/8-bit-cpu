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
  for (int i=D0; i<=CLK; i++) {
    pinMode(i, INPUT);
  }
  Serial.begin(115200);

}

int _clk;
int clk;
bool adr;
bool in;
bool out;
bool up_edge;
bool dn_edge;

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
    byte data = 0;
    for (int pin = D0; pin <= D7; pin += 1) {
      data = (data << 1) + digitalRead(pin);
    }
//    Serial.print(data, DEC);
    Serial.print((char)data);
  }
}
