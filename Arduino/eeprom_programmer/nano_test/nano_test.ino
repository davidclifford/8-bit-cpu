#define RED 2
#define YELLOW 3
#define GREEN 4

void setup() {
  // put your setup code here, to run once:
  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);
  Serial.begin(57600);
}

void blink_led(int led, int dur) {
  digitalWrite(led, HIGH);
  delay(dur);
  digitalWrite(led, LOW);
}
void loop() {
  // put your main code here, to run repeatedly:
  blink_led(random(RED,GREEN+1),random(100,300));
}
