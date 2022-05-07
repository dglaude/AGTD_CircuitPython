# AGTD_CircuitPython
Translation in CircuitPython of AGTD

# Install and customize the code for your board

This require a recent version of CircuitPython (such as 7.3.0-beta.2) and works one a Seeeduino Wio Terminal.
If you don't have a Seeeduino, you can use another board (with enough memory, like an Raspberry Pi Pico), you will just have to modify the button PIN:

BUTTON_PIN = board.BUTTON_3

or disable completely the button and use a delay, here 30 seconds before starting:

NO_BUTTON = False
NO_BUTTON_DELAY = 30

# Usage

From your computer, deposite GTD fils at the root of the CIRCUITPY drive.
Eject the CircuitPython board from your computer and plug it into the Switch.
Make sure you are in Game Builder Garage and in edit mode.
Watch the texture being draw without touching the Switch.

# Credit and Copyright

This code a tentative to translate Arduino code into CircuitPython.
The CircuitPython code is made by David Glaude under MIT
The original Arduino code is by Borri based on an idea from Scrubz

AGTDASAVDCWTSCOVrVam also known more succinctly as AGTD: Automatic GBG Texture Drawing
v0.7-beta
Made for Arduino Leonardo by Borri
Original idea by Scrubz
