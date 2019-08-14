

//System Parameters
int Ts = 0.03; //s  
int V_max = 12; //v
int positivePin = 6;
int negativePin = 5;

//PID Parameters
double kp = 501900;
double Ti = 2.782;
double Td = 0.6956;
double a = kp+Ti*Ts/2 + Td/Ts;
double b = -kp + Ti*Ts/2 - 2*Td/Ts;
double c = Td/Ts;


double angle = 180; 
double ref = 180;
double ek = 0; 
double ek1 = 0; 
double ek2 = 0;
double uk1 = 0;
double uk;

void setup() {
  Serial.begin(115200);
}
 
unsigned int integerValue=0;  // Max value is 65535
char incomingByte;
 //----
void loop() {
  angle = getangle();
  ek = ref-angle;
  uk = PID(uk1, ek, ek1, ek2);
  if(uk < 0)
  {
    analogWrite(negativePin, powerToPWM(-uk));
  }else{
    analogWrite(positivePin, powerToPWM(uk));
  }

  Serial.print(uk);
  
  uk1 = uk;
  ek1 = ek;
  ek2 = ek1;
}
//----
double getangle(){
  if (Serial.available() > 0) {   // something came across serial
    integerValue = 0;         // throw away previous integerValue
    while(1) {            // force into a loop until 'n' is received
      incomingByte = Serial.read();
      if (incomingByte == '\n') break;   // exit the while(1), we're done receiving
      if (incomingByte == -1) continue;  // if no characters are in the buffer read() returns -1
      integerValue *= 10;  // shift left 1 decimal place
      // convert ASCII to integer, add, and shift left 1 decimal place
      integerValue = ((incomingByte - 48) + integerValue);
    }
    Serial.println(integerValue);   // Do something with the value
  }
return integerValue;
}


double PID (double u_k1, double ek, double ek1, double ek2){
  double u = u_k1 + a*ek + b*ek1 + c*ek2;
  return u;
}

double powerToPWM(double u){
  double duty = 255*u/V_max;
}

