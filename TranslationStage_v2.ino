// Steppter motor control for translational stage, 
// based on DualMotorShield.pde
// Auhor: Htoo Wai Htet
// Versin: 2.0

// v_2.0 updates: ability to define which motor to move via the command

#include <AccelStepper.h>

// The Left Stepper pins
#define STEPPERl_DIR_PIN 8
#define STEPPERl_STEP_PIN 11
// The Right stepper pins
#define STEPPERr_DIR_PIN 7
#define STEPPERr_STEP_PIN 10

// Define some steppers and the pins the will use
AccelStepper stepper_l(AccelStepper::DRIVER, STEPPERl_STEP_PIN, STEPPERl_DIR_PIN);
AccelStepper stepper_r(AccelStepper::DRIVER, STEPPERr_STEP_PIN, STEPPERr_DIR_PIN);

char input, remain;
float spd, acl;
int ori, mot;
long dis;

void setup()
{  
    Serial.begin(9600);
}

void loop()
{
  while(!Serial.available()); // poll so that it only prints once
    // while there is something in Serial buffer, parse and read
   while(Serial.available()) {
    char input = Serial.peek();
    // If the indicator is speed
    if (input == 's') {
      Serial.read();
      spd = Serial.parseFloat();
    }
   // If the indicator is acceleration
    else if (input == 'a') {
      Serial.read();
      acl = Serial.parseFloat();
    }
    // If the indicator is distance
    else if (input == 'd') {
      Serial.read();
      dis = Serial.parseInt();
    }
    // If the indicator is orientation
    else if (input == 'o') {
      Serial.read();
      ori = Serial.parseInt(); // 1 = in; 0 = out  
    }
    // If the indicator is the choice of motors
    else if (input == 'm') {
      Serial.read();
      mot = Serial.parseInt();
    }
    else {
      Serial.println("ERROR INPUT");
      char error_input = Serial.read();
      Serial.print("Input cannot contain: ");
      Serial.println(error_input);
      Serial.flush();  // flush the command with error input
    }
  }
  // show the user the collected data & run
  printData(spd, acl, dis, ori, mot);
  runSteppers(spd, acl, dis, ori, mot);
}

void runSteppers(float maxspeed, float acceleration, long distance, int orientation, int mot) {
    ori? distance = -distance: distance = distance;
  
    stepper_l.setMaxSpeed(maxspeed);
    stepper_l.setAcceleration(acceleration);
    stepper_l.move(-distance );
    
    stepper_r.setMaxSpeed(maxspeed);
    stepper_r.setAcceleration(acceleration);
    stepper_r.move(distance);
    
    long l_distToGo = stepper_l.distanceToGo();
    long r_distToGo = stepper_r.distanceToGo();
    
    // not a good way of checking, but it works for now
    if (mot == 0) {
      while (l_distToGo != 0 || r_distToGo != 0) {
        if (l_distToGo != 0) {
          stepper_l.run();
          l_distToGo = stepper_l.distanceToGo();
        }
        if (r_distToGo != 0) {
          stepper_r.run();
          r_distToGo = stepper_r.distanceToGo();
        }
      }
   }
   else if (mot == 1) {  // left motor is chosen
     while (l_distToGo != 0) {
        stepper_l.run();
        l_distToGo = stepper_l.distanceToGo();
     }
   }
   else if (mot == 2) {  // right motor is chosen
     while (r_distToGo != 0) {
        stepper_r.run();
        r_distToGo = stepper_r.distanceToGo();
     }
   }
   else {    // hopefully, this won't happen
     Serial.println("Error in motor choice received");
   }
}

void printData(float spd, float acl, long dis, int ori, int mot) {
  
  switch (mot) {
    case 0:
      Serial.print("Both motors");
      break;
    case 1:
      Serial.print("Left motor");
      break;
    case 2:
      Serial.print("Right motor");
      break;
  }
  Serial.print("\t");
  
  Serial.print("Distance: ");
  Serial.print(dis);
  Serial.print("\t");
  
  Serial.print("Speed: ");
  Serial.print(spd);
  Serial.print("\t");
  
  Serial.print("Acceleration: ");
  Serial.print(acl);
  Serial.print("\t");
  
  Serial.print("Direction: ");
  ori ? Serial.print("Inward"): Serial.print("Outward"); //if-else shorthand
  Serial.println();  
}
