void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

long int awesome_number = 0;
void loop() {
  awesome_number++;
  Serial.print("Hello! ...For the "); 
  Serial.print(awesome_number) ; Serial.println("th time");
  
  delay(500);
  if (Serial.available()){
  String message = Serial.readString();
  Serial.print("Rec'd ");
  Serial.println(message);
  }
}
