/*
Arduino code for just dispensing liquid.
*/

#include <stdio.h>
#include <stdlib.h>
#include <Stepper.h>

#define DISPENSE1 8
#define DISPENSE2 6
#define DISPENSE3 7
#define DISPENSE4 5
#define DISPENSE_CALIBRATE_PIN 2
#define DISPENSER_CONTROLLER_PIN 3
#define DISPENSER_OPEN 100
#define LED_PIN 13

// Motor Specs
const int stepsPerRevolution = 2048;
const double degree = stepsPerRevolution / 360;

// Initialize Stepper Motor
Stepper dispenser(stepsPerRevolution, DISPENSE1, DISPENSE2, DISPENSE3, DISPENSE4);

// Initialize Variables
int dispenserPosition = 0;
bool dispensing = false;
int targetPosition = 0;

void setup() {
    pinMode(DISPENSE_CALIBRATE_PIN, INPUT_PULLUP);
    pinMode(DISPENSER_CONTROLLER_PIN, INPUT_PULLUP);
    pinMode(LED_PIN, OUTPUT);
    dispenser.setSpeed(15);
    attachInterrupt(
        digitalPinToInterrupt(DISPENSE_CALIBRATE_PIN),
        setPositionZeroISR,
        FALLING);
    attachInterrupt(
        digitnalPinToInterrupt(DISPENSER_CONTROLLER_PIN),
        controllerISR,
        CHANGE);
    Serial.begin(9600);
}

void loop() {
    // Check if the dispenser is in use already. Turn on LED if in use.
    if (dispensing) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }
    /* Check target and current position. 
       Adjust to get the current closer to the target.
       Adding too many operations here will increase the duration of
       the loop and may cause the motor to spin very slowly since it
       will spend a lot of time deciding which direction to move only
       to move one step.
    */
    if (targetPosition != dispenserPosition) {
        dispensing = true;
        if (targetPosition > dispenserPosition) {
            dispenser.step(1);
            dispenserPosition += 1;
        } else {
            dispenser.step(-1);
            dispenserPosition -= 1;
        }
    } else {
        dispensing = false;
    }
}

void setPositionZeroISR() {
    dispenserPosition = 0;
}

void controllerISR() {
    if (digitalRead(DISPENSER_CONTROLLER_PIN) == HIGH) {
        /* Button is not pressed since input type is "input_pullup".
           If I want the dispenser to be normally closed, make this a
           closing operation.
        */
        targetPosition = 0;        

    } else { 
        /* The controller pin is reading low.  Which means the button
           is pressed since the input type is "input_pullup".  This 
           means I should make this an opening operation.
        */
        targetPosition = DISPENSER_OPEN;
    }
}

