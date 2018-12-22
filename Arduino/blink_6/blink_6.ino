int led1 = 3;
//int led2 = 4;
//int led3 = 5;
//int d0 = 6;
//int d1 = 7;
//int d2 = 8;
//int d3 = 9;
//int d4 = 10;
//int d5 = 11;
//int d6 = 12;
//int d7 = 13;

void setup() {
  // put your setup code here, to run once:
  pinMode(led1, OUTPUT);
//  pinMode(led2, OUTPUT);
//  pinMode(led3, OUTPUT);
//  pinMode(d0, OUTPUT);
//  pinMode(d1, OUTPUT);
//  pinMode(d2, OUTPUT);
//  pinMode(d3, OUTPUT);
//  pinMode(d4, OUTPUT);
//  pinMode(d5, OUTPUT);
//  pinMode(d6, OUTPUT);
//  pinMode(d7, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  blink_led(led1);
//  blink_led(led2);
//  blink_led(led3);
//  blink_led(d0);
//  blink_led(d1);
//  blink_led(d2);
//  blink_led(d3);
//  blink_led(d4);
//  blink_led(d5);
//  blink_led(d6);
//  blink_led(d7);
}

void blink_led(int led) {
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
  delay(100);
}
