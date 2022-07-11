# AGTD_CircuitPython
Translation in CircuitPython of AGTD

# History and supported board

Initial release was done for the Seeeduino Wio Terminal (code still available in code_wio_terminal.py).
Hint on how to use that on a Pico (that does not have a button) were given.
Later a new release was done specifically for the PyGamer that has special kind of button (not GPIO).

Current release is working on many different board with different MCU and screen:
* [pygamer](https://circuitpython.org/board/pygamer/)
* [clue_nrf52840_express](https://circuitpython.org/board/clue_nrf52840_express/)
* [espressif_esp32s3_usb_otg_n8](https://circuitpython.org/board/espressif_esp32s3_usb_otg_n8/)
* [adafruit_feather_esp32s3_tft](https://circuitpython.org/board/adafruit_feather_esp32s3_tft/)
* [seeeduino_wio_terminal](https://circuitpython.org/board/seeeduino_wio_terminal/)

My test are mostly done on "CircuitPython 8.0.0-alpha.1" or on the bleeding edge version of CircuitPython, but it should work on CircuitPython 7.3.1 if available for your board.

# Customize the code for other board

If this version fail on your board on a divide by zero error `print(42/0)` this mean your board is not explicitly supported.
The best way to have support is to add a section in the board detection and select the button and message specific to your board. Scaling factor will depend on your screen resolution, try or do the math. 

```elif board.board_id in ("your_board_id"):
    MESSAGE="Press A button."
    SCALE=3
    NO_BUTTON = False
    NO_BUTTON_DELAY = 30
    BUTTON_PIN = board.BUTTON_A
    PY_GAMER=False```

If you want a new board to be supported, don't hesitate to create an issue for a specific board, if I have that in stock I might make a version that work for you. If you can create the code for your own board, please try submitting it here as a PR so that is can serve other user.

# Install

You wil need the folowing files from this repository:
* boot.py This define a simple mouse USB HID description that is recognized by the Nintendo Switch
* code.py This is the main code with board detection
* mouseto.py Library to handled absolute mouse move like an Arduino library with same name is doing

The only library required is Adafruit HID library in the form of a folder adafruit_hid and it's content in the lib folder.
You can get that library [from the source](https://github.com/adafruit/Adafruit_CircuitPython_HID) but best is to install that [with circup](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup) or getting it from the [library bundle](https://circuitpython.org/libraries).

# Special version

* `code_pygamer.py` is a version for PyGamer that is not needed anymore as that board is supported in main code with auto-detection.
* `code_wio_terminal.py` is the initial release maybe without graphical interface, could be usefull for adapting for the Raspbery Pi Pico or other very simple board.

# Usage

From your computer, deposite GTD files at the root of the CIRCUITPY drive, if you have none you can use `SwitchColourPatternFixed.GTD` for a first try.
Once you are ready with one or multiple files, eject the CircuitPython board from your computer and plug it into your Nintendo Switch.
Make sure you are in Game Builder Garage and in edit mode in a new or existing game.
Watch the texture being draw without touching the Switch, maybe go get something to drink or do something else, it could take a while.

# How to create GTD image and more

To save time in documenting how to create image in the GTD format, please have a look at this excelent port to the Xiao Seeeduino: https://raycardillo.github.io/automatic-gbg-texture-creator/ (see also https://github.com/raycardillo/automatic-gbg-texture-creator).

# Credit and Copyright

This code a tentative to translate Arduino code into CircuitPython.
The CircuitPython code is made by David Glaude under MIT
The original Arduino code is by Borri based on an idea from Scrubz

AGTDASAVDCWTSCOVrVam also known more succinctly as AGTD: Automatic GBG Texture Drawing
v0.7-beta
Made for Arduino Leonardo by Borri
Original idea by Scrubz

Also a big thank you to @raycardillo for the Xiao version.
