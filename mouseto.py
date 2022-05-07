from adafruit_hid.mouse import Mouse

### vvv ### MouseTo.h
### // MouseTo - Library for Arduino Leonardo/Micro for moving the mouse pointer to absolute screen coordinates: http://github.com/per1234/MouseTo
### #ifndef MouseTo_h
### #define MouseTo_h
###
### #include <Arduino.h>
### #if ARDUINO > 10605
### #include <Mouse.h>
### #endif  //ARDUINO > 10605
###
### class MouseToClass {
###   public:
###     MouseToClass();
###     void setTarget(const int targetXinput, const int targetYinput, const boolean homeFirst = true);
###     int getTargetX();
###     int getTargetY();
###     boolean moveTo(const int targetXinput, const int targetYinput);
###     boolean move();
###     void setScreenResolution(const int x, const int y);
###     unsigned int getScreenResolutionX();
###     unsigned int getScreenResolutionY();
###     void setCorrectionFactor(const float correctionFactorInput);
###     float getCorrectionFactor();
###     void setMaxJump(const int8_t jumpDistanceInput);
###     int8_t getMaxJump();
###     void home();
###   private:
###     int targetX;
###     int targetY;
###     int positionX;
###     int positionY;
###     boolean homed;
###     int screenResolutionX;
###     int screenResolutionY;
###     float correctionFactor;
###     int8_t jumpDistance;
###     boolean moveAxisX;
### };
### extern MouseToClass MouseTo;  //declare the class so it doesn't have to be done in the sketch
### #endif  //MouseTo_h
### ^^^ ### MouseTo.h

### MouseToClass::MouseToClass() {
###   //set default values
###   screenResolutionX = 3840;  //4K UHD
###   screenResolutionY = 2160;  //4K UHD
###   correctionFactor = 1;
###   jumpDistance = 10;  //this seems like a good balance between speed and accuracy
### }
class MouseTo(Mouse):
    screenResolutionX = 3840
    screenResolutionY = 2160
    correctionFactor = 1.0
    jumpDistance = 10
    positionX = 0
    positionY = 0
    targetX = 0
    targetY = 0
    moveAxisX = False
    homed = False


### void MouseToClass::setScreenResolution(const int x, const int y) {
###   screenResolutionX = x;
###   screenResolutionY = y;
### }
    def setScreenResolution(res_x, res_y):      # MouseTo.setScreenResolution(1280,720);
####        print("setScreenResolution(",res_x,", ",res_y,")")
####        global screenResolutionX
####        global screenResolutionY
        MouseTo.screenResolutionX = res_x
        MouseTo.screenResolutionY = res_y


### void MouseToClass::setCorrectionFactor(const float correctionFactorInput) {
###   correctionFactor = correctionFactorInput;
### }
    def setCorrectionFactor(factor):            # MouseTo.setCorrectionFactor(1);
####        global correctionFactor
        MouseTo.correctionFactor = factor


### void MouseToClass::setMaxJump(const int8_t jumpDistanceInput) {
###   jumpDistance = jumpDistanceInput;
### }
    def setMaxJump(max_jump):                   # MouseTo.setMaxJump(127);
####        print("setMaxJump(",max_jump,")")
####        global jumpDistance
        MouseTo.jumpDistance = 10


#        print("screenResolutionX:", MouseTo.screenResolutionX)
#        print("screenResolutionY:", MouseTo.screenResolutionY)
#        print("jumpDistance:", MouseTo.jumpDistance)


### void MouseToClass::setTarget(const int targetXinput, const int targetYinput, const boolean homeFirst) {
###   //convert screen coordinates to Arduino coordinates
###   targetX = targetXinput * correctionFactor;
###   targetY = targetYinput * correctionFactor;
###   homed = !homeFirst;
### }
#    def setTarget(target_x, target_y ):# , homeFirst):          # MouseTo.setTarget(0,0);
    def setTarget(self, target_x, target_y, homeFirst):          # MouseTo.setTarget(0,0);
#        global targetX
#        global targetY
#        global homed
        MouseTo.targetX = target_x
        MouseTo.targetY = target_y
        MouseTo.homed = not homeFirst


### void MouseToClass::home() {
###   homed = false;
### }
    def home():
        MouseTo.homed = False


    def move(self, x: int = 0, y: int = 0, wheel: int = 0):
#        print("move:", x, y, wheel)
        if ((x != 0) or (y != 0) or (wheel != 0)):
#            print("calling move from parent library")
            super().move(x, y, wheel)
            MouseTo.positionX += x
            MouseTo.positionY += y
            return True
        else:
#            print("internal move from MoveTo library")
            if not MouseTo.homed:
#                print("Homing first")
                moveToTargetX = -MouseTo.screenResolutionX - 50
                moveToTargetY = -MouseTo.screenResolutionY - 50
                moveX = moveToTargetX - MouseTo.positionX
                moveY = moveToTargetY - MouseTo.positionY
#                print("move for homing:", moveX, moveY)
                super().move(moveX, moveY)
                MouseTo.positionX = 0
                MouseTo.positionY = 0
                MouseTo.homed = True
            moveToTargetX = MouseTo.targetX
            moveToTargetY = MouseTo.targetY
            moveX = moveToTargetX - MouseTo.positionX #.#
            moveY = moveToTargetY - MouseTo.positionY #.#
#            print("move:", moveX, moveY)
            super().move(moveX, moveY)
            MouseTo.positionX += moveX
            MouseTo.positionY += moveY
            return True
### boolean MouseToClass::move() {
###   //the mouse is homed to 0,0 on each mouse movement to make sure the absolute screen coordinates will be reached even if the physical mouse has been moved since the last moveTo
###   int moveToTargetX;
###   int moveToTargetY;
###   if (homed == false) {
###     //make sure it reaches 0,0 even in the worst case scenario of the cursor being at the bottom right corner
###     moveToTargetX = -screenResolutionX - 50;
###     moveToTargetY = -screenResolutionY - 50;
###   }
###   else {
###     moveToTargetX = targetX;
###     moveToTargetY = targetY;
###   }
###
###   if (positionX != moveToTargetX || positionY != moveToTargetY) {
###     if (positionX != moveToTargetX && (positionY == moveToTargetY || (positionY != moveToTargetY && moveAxisX == true))) {
###       const int moveX = moveToTargetX > positionX ? min(jumpDistance, moveToTargetX - positionX) : max(-jumpDistance, moveToTargetX - positionX);
###       Mouse.move(moveX, 0, 0);
###       positionX += moveX;
###       moveAxisX = false;
###     }
###     else {
###       const int moveY = moveToTargetY > positionY ? min(jumpDistance, moveToTargetY - positionY) : max(-jumpDistance, moveToTargetY - positionY);
###       Mouse.move(0, moveY, 0);
###       positionY += moveY;
###       moveAxisX = true;
###     }
###   }
###   else { //home or target position reached
###     if (homed == false) {  //mouse is homed
###       homed = true;
###       positionX = 0;
###       positionY = 0;
###       return false;
###     }
###     homed = false;  //reset for the next go
###     return true;
###   }
###   return false;
### }




### // MouseTo - Library for Arduino Leonardo/Micro for moving the mouse pointer to absolute screen coordinates: http://github.com/per1234/MouseTo
### #include "MouseTo.h"

### int MouseToClass::getTargetX() {
###   return targetX;
### }

### int MouseToClass::getTargetY() {
###   return targetY;
### }

### //used for compatibility with the previous API
### boolean MouseToClass::moveTo(const int targetXinput, const int targetYinput) {
###   setTarget(targetXinput, targetYinput);
###   return move();
### }


### unsigned int MouseToClass::getScreenResolutionX() {
###   return screenResolutionX;
### }

### unsigned int MouseToClass::getScreenResolutionY() {
###   return screenResolutionY;
### }

### float MouseToClass::getCorrectionFactor() {
###   return correctionFactor;
### }

### void MouseToClass::setMaxJump(const int8_t jumpDistanceInput) {
###   jumpDistance = jumpDistanceInput;
### }

### int8_t MouseToClass::getMaxJump() {
###   return jumpDistance;
### }

### void MouseToClass::home() {
###   homed = false;
### }

### MouseToClass MouseTo;  //This sets up a single global instance of the library so the class doesn't need to be declared in the user sketch and multiple instances are not necessary in this case.
