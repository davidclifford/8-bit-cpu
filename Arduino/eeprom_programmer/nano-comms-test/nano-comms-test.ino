void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
}

char string[100];

void loop() {
  char x;
  String nano = "From nano ";
  // put your main code here, to run repeatedly:
  x = Serial.read();
  Serial.println(nano + " " + x);
  delay(1000);
}
