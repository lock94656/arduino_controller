void setup() {
  Serial.begin(115200);

  pinMode(2, INPUT_PULLUP); // X
  pinMode(3, INPUT_PULLUP); // Y
  pinMode(4, INPUT_PULLUP); // B
  pinMode(5, INPUT_PULLUP); // A
}

void loop() {
  int x = analogRead(A4); // Joystick horizontal
  x = analogRead(A4);
  int y = analogRead(A1); // Joystick vertical
  y = analogRead(A1);
  
  int boutonX = digitalRead(2);
  int boutonY = digitalRead(3);
  int boutonB = digitalRead(4);
  int boutonA = digitalRead(5);

  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.print(boutonX);
  Serial.print(",");
  Serial.print(boutonY);
  Serial.print(",");
  Serial.print(boutonB);
  Serial.print(",");
  Serial.println(boutonA);

  delay(50);
} 

