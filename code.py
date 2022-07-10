# SPDX-FileCopyrightText: 2022 David Glaude
# SPDX-License-Identifier: MIT

# This version is crafted to support only 4 different CP board (three from Adafruit and one from Espressif).
# The common things those board have is a screen and at least one button.
# The code will wait for the right button to be pressed before acting as a mouse.
# Here is the selected button and the supported board:
#D9 (Start)	"pygamer"
#BUTTON_A	"clue_nrf52840_express"
#BUTTON_OK	"espressif_esp32s3_usb_otg_n8"
#BUTTON (boot)	"adafruit_feather_esp32s3_tft"
#
# It should be easy to port this to other board, just adding the detection code and selecting the button to use.
#

import gc
import os
import time
import board
import usb_hid
import digitalio
from MouseTo import MouseTo
from digitalio import DigitalInOut, Direction

import displayio

all_colors=[
    0xffffff, 0xededed, 0xd9d9d9, 0xf3e6ff, 0xdcb3ff, 0xc685ff, 0xe6fbff, 0xccf7ff, 0x85ebff, 0xf7ffe6, 0xe6ffb3, 0xd6ff85, 0xffe6e6, 0xffb3b3, 0xff8585,
	0xb5b5b5, 0x909090, 0x6c6c6c, 0x8800ff, 0x520099, 0x29004d, 0x00d5ff, 0x00aacc, 0x006b80, 0xaaff00, 0x90d900, 0x558000, 0xff0000, 0xcc0012, 0x800000,
	0x484848, 0x303030, 0x000000, 0xbb98d9, 0x846d99, 0x5b5266, 0x98ced9, 0x5a7a80, 0x36484d, 0xc4d998, 0x89996c, 0x3d4d1f, 0xd95757, 0x804040, 0x4d1f1f,
    0x000000, 0x000000, 0x000000, 0xfee6ff, 0xfbb3ff, 0xf985ff, 0xe6f2ff, 0xb3d6ff, 0x85beff, 0xccffd3, 0x99ffaa, 0x66ff7e, 0xfff0e6, 0xffd3b3, 0xffb885,
    0x000000, 0x000000, 0x000000, 0xf200ff, 0xc200cc, 0x7a0080, 0x1080ff, 0x005fcc, 0x003c80, 0x00D924, 0x009919, 0x00590e, 0xff6a00, 0xcc5500, 0x803500,
    0x000000, 0x000000, 0x000000, 0xd698d9, 0x7d4080, 0x4b1f4d, 0x98b6d9, 0x405e80, 0x1f344d, 0x86bf90, 0x598060, 0x1f3323, 0xd9b398, 0x805b40, 0x4d321f,
    0x000000, 0x000000, 0x000000, 0xffe6f5, 0xffb3df, 0xff85cc, 0xe8e6ff, 0xd0ccff, 0xa199ff, 0xe6fffa, 0xb3fff0, 0x85ffe7, 0xfffde6, 0xfffab3, 0xfff785,
    0x000000, 0x000000, 0x000000, 0xff0095, 0xcc0077, 0x80004b, 0x1500ff, 0x0f00b3, 0x07004d, 0x00ffcf, 0x00cca3, 0x008066, 0xffee00, 0xccbe00, 0x807700,
    0x000000, 0x000000, 0x000000, 0xd998be, 0x80536d, 0x4d1f3a, 0xb2aed9, 0x656282, 0x3b3a4d, 0x98d9cc, 0x6b9990, 0x1f4d43, 0xbfbb86, 0x807e5a, 0x4d4b32]

def delay(mili):
    time.sleep(mili/1000)

debug = True
debug = False

m = MouseTo(usb_hid.devices)

# This code a tentative to translate Arduino code into CircuitPython.
# The CircuitPython code is made by David Glaude under MIT
# The original Arduino code is by Borri based on an idea from Scrubz
# Everything after a triple # is the original code

##_001_## /* -----------------------------------------------------------------------------------------
### * AGTDASAVDCWTSCOVrVam also known more succinctly as AGTD: Automatic GBG Texture Drawing
### * v0.7-beta
### * Made for Arduino Leonardo by Borri
### * Original idea by Scrubz
### *
### * IMPORTANT DEPENDENCIES:
### * Libraries Dependency:    MouseTo by per1234 https://github.com/per1234/MouseTo/
### * You can download libraries dependencies under Arduino Official IDE [Tools]/[Manage Libraries]
### *
### * AGTDASAVDCWTSCOVrVam is licensed under the MIT License
### * ------------------------------------------------------------------------------------------*/
###
###
### /*------------------------------------------------------------------------------------------
### *                                          CONFIG
### * ------------------------------------------------------------------------------------------
### * NO_BUTTON
### * If don't have a button, or a wire to simulate it, to connect to the Arduino Leonardo
### * You must un-comment both lines:
### *     #define NO_BUTTON                 No Wire Option
### *     #define NO_BUTTON_DELAY   30      No Wire Option. Delay time before the program
### *                                       takes control of the mouse. Represented in seconds
### * ------------------------------------------------------------------------------------------
###
### //  #define NO_BUTTON
### //  #define NO_BUTTON_DELAY   30
###
### /*------------------------------------------------------------------------------------------
### * If button/Wire is present, define the Arduino input board PIN
### * Default option:
### *    #define BUTTON_PIN    9           Button input set to Leonardo pin 9
### * ------------------------------------------------------------------------------------------*/
###
### #define BUTTON_PIN    9
#BUTTON_PIN = board.BUTTON_3
#BUTTON_PIN = board.GP9

if board.board_id in ("pygamer"):
    MESSAGE="Press start."
    SCALE=2
    NO_BUTTON = False
    NO_BUTTON_DELAY = 30
    BUTTON_PIN = board.D9
    PY_GAMER=True       # Special button on PyGamer
elif board.board_id in ("clue_nrf52840_express"):
    MESSAGE="Press A button."
    SCALE=3
    NO_BUTTON = False
    NO_BUTTON_DELAY = 30
    BUTTON_PIN = board.BUTTON_A
    PY_GAMER=False
elif board.board_id in ("espressif_esp32s3_usb_otg_n8"):
    MESSAGE="Press OK button."
    SCALE=3
    NO_BUTTON = False
    NO_BUTTON_DELAY = 30
    BUTTON_PIN = board.BUTTON_OK
    PY_GAMER=False
elif board.board_id in ("adafruit_feather_esp32s3_tft"):
    MESSAGE="Press button."
    SCALE=2
    NO_BUTTON = False
    NO_BUTTON_DELAY = 30
    BUTTON_PIN = board.BUTTON
    PY_GAMER=False
else:
    MESSAGE="No button, just wait."
    SCALE=3
    NO_BUTTON = True
    NO_BUTTON_DELAY = 60
    print(42/0)

###
###
### /*------------------------------------------------------------------------------------------
### * MASK - Use "mask" mode
### * This mode is less pleasing to watch draw but improves the speed of the general
### * process.
### *    #define MASK_ENABLED
### * ------------------------------------------------------------------------------------------*/
###
### #define MASK_ENABLED
MASK_ENABLED = False

s_mask = bytearray(513)

### // Scrubz bitwise functions
def mask_reset():
    for i in range(513):
        s_mask[i] = 0

def mask_set(index):
    s_mask[index // 8] |= 1 << index % 8

def mask_get(index):
    return (not (not (1 << index % 8 & s_mask[index // 8])))

### /*------------------------------------------------------------------------------------------
### * SLOW MODE - For projects with a lot of nodon a delay has to be added to avoid lag induced
### * miss-clicks on the GBG Program screen. Recommended values are:
### *
### * Recommended option for new GBG projects (Programming screen with minimal lag):
### *    int delay_move = 0;
### *    int delay_mouse = 0;
### *
### * Recommended option for existing GBG projects (Programming screen with medium-high lag):
### *    int delay_move = 20;
### *    int delay_mouse = 50;
### *
### * Adjust "delay_move" and "delay_mouse" values if you still encounter problems.
### * ------------------------------------------------------------------------------------------*/
###
### int delay_move = 20;
### int delay_mouse = 50;
#delay_move = 20
#delay_mouse = 50
delay_move = 0
delay_mouse = 0

led = digitalio.DigitalInOut(board.LED)             ###   pinMode(LED_BUILTIN, OUTPUT);
led.direction = digitalio.Direction.OUTPUT

list_image = []

image_index = 0
image = bytearray(4097)

def DisplayImage():
    bitmap = displayio.Bitmap(64, 64, 135)
    palette = displayio.Palette(len(all_colors))
    for i in range(len(all_colors)):
        palette[i] = all_colors[i]
    my_index=1
    for y in range(64):
        for x in range(64):
            bitmap[x, y] = image[my_index]
            my_index += 1
    lcd = board.DISPLAY
    screen = displayio.Group(scale = SCALE)
    centerx = (( board.DISPLAY.width - 64*SCALE ) // 2) // SCALE
    centery = (( board.DISPLAY.height - 64*SCALE ) // 2) // SCALE
    bg = displayio.TileGrid(bitmap, pixel_shader=palette, x=centerx, y=centery)
    screen.append(bg)
    lcd.show(screen)


def DisplayAllImage():
    for n, fullpath in enumerate(list_image):
        print("Displaying ", fullpath)
        load_image(fullpath)
        DisplayImage()
        time.sleep(10)


actual_pixel=0                              ### byte actual_pixel;
last_pixel=0                                ### byte last_pixel;
used_colors=bytearray(135)                  ### byte used_colors[135];
used_colors_pointer = 0                     ### byte used_colors_pointer = 0;
used_color=False                            ### bool used_color;
pos_x = 0                                   ### int pos_x;
pos_y = 0                                   ### int pos_y;

def setup():                                ### void setup(void) {
    global led

###   Mouse.begin();
    MouseTo.setScreenResolution(1280,720);
    MouseTo.setCorrectionFactor(1);
    MouseTo.setMaxJump(127);

    print("Working on button.")
    if NO_BUTTON:
        print("NO_BUTTON => wait for some seconds: ", NO_BUTTON_DELAY)
        delay(NO_BUTTON_DELAY*1000)
    else:
        print(MESSAGE)
        if PY_GAMER:
            from adafruit_pybadger import pybadger as panel
            while not panel.button.start:
                led.value = not led.value
                time.sleep(0.2)                                 ###     delay(500);
        else:
            button = DigitalInOut(BUTTON_PIN)                   ###   pinMode(BUTTON_PIN, INPUT_PULLUP);
            button.switch_to_input(pull=digitalio.Pull.UP)
            while button.value:
                led.value = not led.value
                time.sleep(0.2)                                 ###     delay(500);
        print("It will start in 30 seconds.")
        led.value = True
        time.sleep(30)
        led.value = False
        print("Starting.")
###   }

                                        ###   // First move to get real mouse position
    m.setTarget(0,0, True)              ###   MouseTo.setTarget(0,0);
    while not m.move(): pass            ###   while (MouseTo.move() == false) {}
    delay(1000)                         ###   delay(1000);
                                        ### }


def loop():                         ### void loop() {
    global led
    global image
    global image_index
    global used_colors_pointer
    global actual_pixel
    global last_pixel
    global used_colors
    global used_colors_pointer
    global used_color
    global pos_x
    global pos_y


    for n, fullpath in enumerate(list_image):       ###   for (int n=0; n<num_textures; n++) {
        start_loop=time.monotonic()
        load_image(fullpath)                        # Load the GTD file into image[]
        DisplayImage()                              # Convert image[] into a bitmap show in displayio
        createTextureNodon(n)                       ###     createTextureNodon(n);
        clearUsedColorsArray()                      ###     clearUsedColorsArray();
        actual_pixel=image[0]                       ###     actual_pixel = pgm_read_byte_near(image + (image_index*4097) );
    ###
    ###     // --------------------------------------------------------------------------------------------------------------------
    ###
        if actual_pixel!=47:            ###     if (actual_pixel!=47) {       //As new textures has a transparent background we don't have to fill-bucket the canvas if the most used color is "transparent"
            moveMouseTo(1187, 544)      ###       moveMouseTo(1187, 544);     //Mouse click to open  "Palette gear tool/Colour Palette"
            getColor(actual_pixel)      ###       getColor(actual_pixel);     //Get color from the Palette
            moveMouseTo(1221, 55)       ###       moveMouseTo(1221, 55);      //Mouse click on "X" to exit palette
            moveMouseTo(958, 268)       ###       moveMouseTo(958, 268);      //Mouse click on "Bucket Tool"
            moveMouseTo(809, 277)       ###       moveMouseTo(809, 277);      //Just giving a close coord over the canvas to click-fill the background
            moveMouseTo(991, 196)       ###       moveMouseTo(991, 196);      //Mouse click on "Pencil Tool"
                                        ###     }
    ###
        used_colors[used_colors_pointer] = actual_pixel         ###     used_colors[used_colors_pointer] = actual_pixel;           //Add color to the used colors array
        used_colors_pointer+=1                                  ###     used_colors_pointer++;                                     //Update 'pointer'
                                                                ###
        if n==0 :                                               ###     if (n==0) {                                                //Only click on pixel brush first time if multiple textures
            moveMouseTo(940, 375)                               ###       moveMouseTo(940, 375);                                   //Mouse click on "Pixel Brush"
                                                                ###     }
        mask_reset()	                                        ##_245_##   mask_reset();
        for index in range(1, 4097):                            ##_246_##   for (int index=1; index<4097; index++) {
            if (image[index] == actual_pixel):                  ##_252_##               if (pgm_read_byte_near(image + (image_index*4097) + index)==actual_pixel) {
                mask_set(index)                                 ##_253_##             mask_set(index);                             // 'true' values if it's the background color
                                                                ###
        for index in range(1, 4097):                            ##_261_##     for (int index=1; index<4097; index++) {
            pixel_color = image[index]                          ##_266_##       byte pixel_color = pgm_read_byte_near(image + (image_index*4097)+ index);
            used_color=False                                    ##_269_##       used_color = false;
            for j in range(134):                                ###       for (int j=0; j<134; j++) {
                if (used_colors[j] == pixel_color):             ###         if(used_colors[j] == pixel_color) {
                    used_color = True                           ###           used_color = true;
                    break                                       ###           break;
                                                                ###         }
                                                                ###       }
                                                                ###
            if not used_color:                                  ###       if (!used_color) {
                #print("NOT used_color detected:", index, pixel_color, used_colors_pointer)
                used_colors[used_colors_pointer]=pixel_color    ###         used_colors[used_colors_pointer] = pixel_color;
                used_colors_pointer+=1                          ###         used_colors_pointer++;
                moveMouseTo(1187, 544)                          ###         moveMouseTo(1187, 544);              //Mouse click to open  "Palette gear tool/Colour Palette"
                getColor(pixel_color)                           ###         getColor(pixel_color);               //Get color from the Palette
                moveMouseTo(1221, 55)                           ###         moveMouseTo(1221, 55);               //Mouse click on "X" to exit palette
                delay(delay_mouse)                              ###         delay(delay_mouse);
                                                                ###
                k = index                                       ##_287_1##         for (int k=index; k<4097; k++) {
                while (k<4097):                                 ##_287_2##
                    pixelData = image[k]                        ###           byte pixelData = pgm_read_byte_near(image + (image_index*4097)+ k);
                                                                ###
                    if (pixelData == pixel_color):              ##_295_##           if (pixelData == pixel_color) {
                        pos_x = (k-1) % 64                      ##_296_##             pos_x = (k-1) % 64;
                        pos_y = (k-1) // 64                     ##_297_##             pos_y = (k-1) / 64;
                        m.setTarget(340+(pos_x*8), 158+(pos_y*8), False)                                        ###             MouseTo.setTarget(340+(pos_x*8), 158+(pos_y*8), false);
                        while not m.move(): pass                ###             while (MouseTo.move() == false) {}  delay(70+delay_move);
                        delay(70+delay_move)                    ###
                        pressLEFT()                             ###             Mouse.press(MOUSE_LEFT);
                        delay(40+delay_move)                    ###             delay(40+delay_mouse);
                                                                ###
                        mask_set(k)                             ##_304_##       mask_set(k);
                        pos_x = -1                              ##_305_##       pos_x = -1;
                                                                ###
                        line = 0                                ##_308_##             int line = 0;
                        while ((k-1)//64 == (k//64)):           ##_309_##             while ((k-1)/64 == k/64) {
                            pixelData = image[k+1]              ##_332_##               pixelData = pgm_read_byte_near(image + (image_index*4097) + k + 1);
                            if((pixelData == pixel_color) or (mask_get(k+1) == False)):       ###              if (pixelData == pixel_color || mask_get(k+1)==false) {
                                if(pixelData == pixel_color):   ###                if (pixelData == pixel_color) {
                                    mask_set(k+1)               ###                  mask_set(k+1);
                                    pos_x = k % 64              ###                  pos_x = k % 64;
#                                    m.setTarget(340+(pos_x*8), 158+(pos_y*8), False)    ###  force move here to make sure we go on every pixel ###
#                                    m.move()                    ### force move here to make sure we go on every pixel ###
                                                                ###                }
                                line+=1                         ##_339_##                 line++;
                                k+=1                            ##_340_##                 k++;
                            else:                               ##_341_##               } else {
                                break                           ##_342_##                 break;
                                                                ###               }
                                                                ###             }
                        if (line>0):                            ###             if (line>0) {
                            pos_x = (k-1) % 64                  ###               pos_x = (k-1) % 64;
                            m.setTarget(340+(pos_x*8), 158+(pos_y*8), False)    ###               MouseTo.setTarget(340+(pos_x*8), 158+(pos_y*8), false);
                            while not m.move(): pass            ###               while (MouseTo.move() == false) {}  delay(40+delay_move);
                            delay(40+delay_move)                ###
                                                                ###             }
                                                                ###
                        releaseLEFT()                           ###             Mouse.release(MOUSE_LEFT); delay(35+delay_mouse);
                        delay(35+delay_move)                    ###
                                                                ###           }
                                                                ###         }
                                                                ###       }
                    k+=1                                        ##_287_3##
                                                                ###     }
        moveMouseTo(1221, 55);                                  ###     moveMouseTo(1221, 55);      //Mouse click on "X" to exit palette
        delay(delay_mouse);                                     ###     delay(delay_mouse);
        image_index+=1                                          ###     image_index++;
        stop_loop=time.monotonic()
        print("File ", fullpath, " take:", stop_loop-start_loop)
                                                                ###   }
                                                                ###   }
###
### }


### // Aux functions
### // ----------------------------------------------------------------------------------------------------


def pressLEFT():
    global m
    if debug:
        print("press LEFT")
    else:
        m.press(MouseTo.LEFT_BUTTON)


def releaseLEFT():
    global m
    if debug:
        print("release LEFT")
    else:
        m.release(MouseTo.LEFT_BUTTON)


def clickMouse():                                   ### void clickMouse() {
    if debug:
        print("click")
    else:
        delay(70+delay_move)                        ###   delay(70+delay_move);
        m.press(MouseTo.LEFT_BUTTON)                ###   Mouse.press(MOUSE_LEFT);
        delay(40+delay_mouse)                       ###   delay(40+delay_mouse);
        m.release(MouseTo.LEFT_BUTTON)              ###   Mouse.release(MOUSE_LEFT);
        delay(40+delay_mouse)                       ###   delay(40+delay_mouse); }


def moveMouseTo(x, y):                              ### void moveMouseTo (int x, int y) {
    m.setTarget(x, y, False)                        ###   MouseTo.setTarget(x, y, false);
    while not m.move(): pass                        ###   while (MouseTo.move() == false) {}
    clickMouse()                                    ###   clickMouse(); }


def createTextureNodon(n):                          ### void createTextureNodon(byte n) {
    m.setTarget(948, 694, False)                    ###   MouseTo.setTarget(948, 694, false);
    while not m.move(): pass                        ###   while (MouseTo.move() == false) {}
    if n==0:                                        ###   if (n==0) {
        for i in range(16): clickMouse()            ###     for (byte i=0; i<16; i++) clickMouse();
    else:                                           ###   } else {
        for i in range(2): clickMouse()             ###     for (byte i=0; i<2; i++) clickMouse();
                                                    ###   }
    moveMouseTo(358, 694)                           ###   moveMouseTo(358, 694);      //Objects
    moveMouseTo(358, 330)                           ###   moveMouseTo(358, 330);      //Special Objects
    moveMouseTo(488, 570)                           ###   moveMouseTo(488, 570);      //Texture
    delay(300+delay_move)                           ###   delay(300+delay_move);      // An small delay to be sure the nodon is being created due possible lag on the code screen
    moveMouseTo(550, 568)                           ###   moveMouseTo(550, 568);      //Edit Texture Gear icon
                                                    ### }


def clearUsedColorsArray():                         ### void clearUsedColorsArray() {
    global used_colors_pointer
    global used_colors
    used_colors_pointer = 0                         ###   used_colors_pointer = 0;
    for i in range(1, 135):                         ###   for (byte i=0; i<135; i++) {
        used_colors[i]=255                          ###     used_colors[i]=255;      //set initial value to a not existing color


def getColor(color_pos):                            ### void getColor(int color_pos){
    column = color_pos % 15                         ###   int column = color_pos % 15;
    row = color_pos // 15                           ###   int row = color_pos / 15;
    pos_x = (int) (84+(column*48)+((column//3)*16)) ###   int pos_x = 84+(column*48)+((column/3)*16);
    pos_y = (int) (175+(row*48)+((row//3)*16))      ###   int pos_y = 175+(row*48)+((row/3)*16);
    moveMouseTo(pos_x, pos_y)                       ###   moveMouseTo(pos_x, pos_y);      //Move mouse to color coords. and click on it


def load_image(fullpath):
    global image
    file = open(fullpath, "rb")
    image = file.read(4097)
    file.close()

def add_GTD_file(path):
    global list_image
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if not isdir:
            if filesize == 4097:
                if file.lower().endswith('.gtd'):
                    list_image += [path + "/" + file]

add_GTD_file("")

print(list_image)

setup()                                             ### Arduino
loop()                                              ### Arduino

while True:                                         ###   while(1) {
    led.value = True                                ###     digitalWrite(LED_BUILTIN, HIGH);
    time.sleep(1)                                   ###     delay(500);
    led.value = False                               ###     digitalWrite(LED_BUILTIN, LOW);
    time.sleep(1)                                   ###     delay(500);

