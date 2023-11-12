//------------------------------------//
//----- program for ME2-HMTX Lab1-----//
//---output digital port 3,5,6,9------//
//--- Coding via Arduino UNO ---------//
//------------------------------------//

//'set output pins
int pin_num[] = {3, 5, 6, 9};                           // Digital Output pin number

//Program Variable
unsigned int num = 0;                                   // Display value, It should be range from 0-15;
unsigned int bit1 = 0, bit4 = 0 , bit2 = 0, bit3 = 0;   // Bits Value
unsigned int rem_bit1 = 0, rem_bit4 = 0 , rem_bit2 = 0, rem_bit3 = 0;   // remainder bits value in each digit


// Initial Setup
// put your setup code here, to run once:
void setup() {
  pinMode(pin_num[0], OUTPUT);        // set pin X as an output pin
  pinMode(pin_num[1], OUTPUT);
  pinMode(pin_num[2], OUTPUT);
  pinMode(pin_num[3], OUTPUT);        

  // Init serial Communication for Serial Digital Oscilloscope
  Serial.begin(9600);               // Inital Serial communication at X Baudrate
}

void loop() {
  num = 9 ;                 // Set value from 0-15
  num2nibble(num);          // this function is change number,"num",from value 0-15 into 4 bits digital number
}

void num2nibble(int num)
{
  bit1        = num / 2;            
  rem_bit1    = num % 2;
  bit2        = bit1 / 2;
  rem_bit2    = bit1 % 2;
  bit3        = bit2 / 2;
  rem_bit3    = bit2 % 2;
  bit4        = bit3 / 2;
  rem_bit4    = bit3 % 2;
  //Set digital output pin to 0 or 1 ( 0V or 5V)
  digitalWrite(pin_num[0], rem_bit1);           //set pin_num[0] to 0 or 1. in this case, it is bit1
  digitalWrite(pin_num[1], rem_bit2);           //set pin_num[1] to 0 or 1
  digitalWrite(pin_num[2], rem_bit3);           //set pin_num[2] to 0 or 1
  digitalWrite(pin_num[3], rem_bit4);           //set pin_num[3] to 0 or 1. in this case, it is bit4
}
