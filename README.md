# AGTD_CircuitPython
Translation in CircuitPython of AGTD

# Install

This require a recent version of CircuitPython (such as 7.3.0-beta.2) and works on a Seeeduino Wio Terminal.
Do go and acquire a Wio Terminal for this project, check if you don't already have a board that support CircuitPython: https://circuitpython.org/downloads
If you avoid M0 board, you should be OK with most board that have native USB (=most) and enough memory.
Don't hesitate to create an issue for a specific board, if I have that in stock I might make a version that work for you, or share your experience if you succeed.

# customize the code for your board

If you don't have a Seeeduino, you can use another board (with enough memory, like an Raspberry Pi Pico), you will just have to modify the button PIN:

BUTTON_PIN = board.BUTTON_3

or disable completely the button and use a delay, here 30 seconds before starting:

NO_BUTTON = False
NO_BUTTON_DELAY = 30

# Special version for PyGamer

The existing code.py is functional and can be adapted for various board with or without button.

But the PyGamer does not have it's button mapped directly to GPIO, so it require special treatement and library.

Since future developement might include hardware detection and displaying the texture on screen if available, I made a special version for the PyGamer

Please use code_pygamer.py and rename it into code.py (overwirting the simple version) if you have a PyGamer (migth work on a PyBadge)

# Usage

From your computer, deposite GTD files at the root of the CIRCUITPY drive, if you have none you can use `SwitchColourPatternFixed.GTD` for a first try.
Once you are ready with one or multiple files, eject the CircuitPython board from your computer and plug it into your Nintendo Switch.
Make sure you are in Game Builder Garage and in edit mode in a new or existing game.
Watch the texture being draw without touching the Switch, maybe go get something to drink or do something else, it could take a while.

# How to create GTD image and more

To save time in documenting how to create image in the GTD format, please have a look at this excelent port to the Xiao Seeeduino: https://raycardillo.github.io/automatic-gbg-texture-creator/ (see also https://github.com/raycardillo/automatic-gbg-texture-creator).

Since I have a Xiao and it is supported by CircuitPython (https://circuitpython.org/board/seeeduino_xiao/), I might make a version for it too. :-)

# Credit and Copyright

This code a tentative to translate Arduino code into CircuitPython.
The CircuitPython code is made by David Glaude under MIT
The original Arduino code is by Borri based on an idea from Scrubz

AGTDASAVDCWTSCOVrVam also known more succinctly as AGTD: Automatic GBG Texture Drawing
v0.7-beta
Made for Arduino Leonardo by Borri
Original idea by Scrubz

Also a big thank you to @raycardillo for the Xiao version.
