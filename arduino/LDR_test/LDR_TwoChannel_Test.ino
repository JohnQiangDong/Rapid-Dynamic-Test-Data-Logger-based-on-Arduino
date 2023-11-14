#include <stdio.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200);
}

void loop() {
  float LDR_Reading_1 = 0;
  float LDR_Reading_2 = 0;
  int int_part_1 = 0;
  int frac_part_1 = 0;
  int int_part_2 = 0;
  int frac_part_2 = 0;
  char buf_1[3];
  char buf_2[3];
  // put your main code here, to run repeatedly:
  LDR_Reading_1 = (float)analogRead(A0);
  LDR_Reading_2 = (float)analogRead(A7);
  frac_part_1 = (LDR_Reading_1 * 100) * (3.3/1024) - int_part_1 * 100; //code to calculate the fractions part of a ADC value
  int_part_1 = LDR_Reading_1 * (3.3/1024);
  sprintf(buf_1,"%d.%02d",int_part_1,frac_part_1);// and format as a string using sprintf
  frac_part_2 = (LDR_Reading_2 * 100) * (3.3/1024) - int_part_2 * 100; //code to calculate the fractions part of a ADC value
  int_part_2 = LDR_Reading_2 * (3.3/1024);
  sprintf(buf_2,"%d.%02d",int_part_2,frac_part_2);// and format as a string using sprintf
  Serial.println(buf_1);
  Serial.println(buf_2);
  delay(100);
}