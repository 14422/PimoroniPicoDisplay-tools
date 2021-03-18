import framebuf
import picodisplay as display
from struct import * # for 'unpack_from'
import utime # for timer

# This is the converted image result you should have on your Pico
from Botw128 import *

# Create an object from the image class of the converted image. The class name is always image name + Class
botw128 = Botw128Class()

# Init screen stuff
screenWidth = display.get_width()
screenHeight = display.get_height()

display_buffer = bytearray(screenWidth * screenHeight * 2)
display.init(display_buffer)

display.set_backlight(1.0)
display.clear()

# Init timers
startTime = utime.ticks_ms()
stopTime = utime.ticks_ms()


# Sets drawing color to given RGB values
def SetPen(rgb):
    display.set_pen(rgb[0], rgb[1], rgb[2])
    
def StartTimer():
    startTime = utime.ticks_ms()

def StopTimer(image):
    stopTime = utime.ticks_ms()
    print("Drawing image '", image.ImageName, "' took " , utime.ticks_diff(stopTime, startTime), "ms")

# Draws the given image into x and y offset values. Additional True boolean can be given to also print the duration for the whole operation
def DrawPackedimage(image, xOffset, yOffset, TakeTime = False):
    
    if TakeTime:
        StartTimer()
    
    # Get the image width
    imageWidth = image.ImageWidth

    # Get the amount of packed colors there are in the hex array = drawing actions needed
    drawingActions = image.ImagePackedColorCount
        
    x = xOffset # x = Starting offset
    y = yOffset # y = Starting offset
    
    for i in range(drawingActions):

        # Unpack drawing actions one by one. Inputs are like [315, 2]. so 315 pixels with color number 2
        actionToDraw = unpack_from('BB', image.HexArray, i*2)
        pixelsToDraw = actionToDraw[0]
        colorToUse = actionToDraw[1]
        
        # While there are more or just enough pixels to fill one row of the image, loop some full row drawing
        while pixelsToDraw >= imageWidth - x + xOffset:
            pixelsTillBorder = imageWidth - x  + xOffset          
            
            # Check that the color to be used is not transparent
            if (image.ColorList[colorToUse][3] != 0):
                
                # Set the correct color
                rgb = (image.ColorList[colorToUse][0], image.ColorList[colorToUse][1], image.ColorList[colorToUse][2])
                SetPen(rgb)
                
                # Draw a line with given pixel amount
                display.pixel_span(x,y, pixelsTillBorder)                

            y += 1
            x = 0 + xOffset
            pixelsToDraw -= pixelsTillBorder
        
        # Full rows are drawn now so we draw what's left, if any

        # Skip transparent colors again
        if (image.ColorList[colorToUse][3] != 0):

            # Set the correct color
            rgb = (image.ColorList[colorToUse][0], image.ColorList[colorToUse][1], image.ColorList[colorToUse][2])
            SetPen(rgb)
            
            # Draw a line with given pixel amount
            display.pixel_span(x, y, pixelsToDraw)
            
        x += pixelsToDraw
        
    if TakeTime:
        StopTimer(image)

# Clear screen with black
display.set_pen(0,0,0)
display.clear()

# Draw the image
DrawPackedimage(botw128, 0, 0, True)
display.update()


