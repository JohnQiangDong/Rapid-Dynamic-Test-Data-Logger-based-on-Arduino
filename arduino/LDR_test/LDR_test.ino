#include <stdio.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
}

void loop() {
  float LDR_Reading = 0;
  int int_part = 0;
  int frac_part = 0;
  char buf[3];
  // put your main code here, to run repeatedly:
  LDR_Reading = (float)analogRead(A0);
  frac_part = (LDR_Reading * 100) * (3.3/255) - int_part * 100; //code to calculate the fractions part of a ADC value
  int_part = LDR_Reading * (3.3/255);
  sprintf(buf,"%d.%02d",int_part,frac_part);// and format as a string using sprintf
  //Serial.println(buf);
  delay(0.1);
}
