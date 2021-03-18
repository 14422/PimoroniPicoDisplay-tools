import sys
import cv2
import sys
import array
from struct import *

inputFile = sys.argv[1]

# Get input file
fileName = inputFile.split(".")[0]

# Output file will be created as (image name) + Image.py, For example: CarImage.py
f = open(fileName + ".py", 'w')

# Hex values will be stored in array
f.write("import array\r\n")

# Read colors from input file and convert from BRGA to RGBA order
BRGA = cv2.imread(inputFile, cv2.IMREAD_UNCHANGED)
RGBA = cv2.cvtColor(BRGA, cv2.COLOR_BGRA2RGBA)

# Get height and width of the image
h, w = RGBA.shape[:2]

allColors = []

# Collect all pixel colors in RGBA as hex
for x in range(h):
    for y in range(w):
    	allColors.append('(0x{:02x}{:02x}{:02x}{:02x})'.format(RGBA[x,y][0],RGBA[x,y][1],RGBA[x,y][2],RGBA[x,y][3]))

colorDictionary = {}

# Save the hex format
hexColors = allColors

# Leave only unique colors to the hex list
hexColors = set(hexColors)

# Sort hex colors so that they will be always at the same order if generated again
hexColors = sorted(hexColors)

# Map all unique colors to a dictionary
for index, color in enumerate(hexColors):
	colorDictionary.update({index : color})

# Create an int list of all unique colors
rev = { v:k for k,v in colorDictionary.items()}
allColorsAsInt = [rev[item] for item in allColors]

# Print all colors as hex for debugging
#print(allColors)

# Horizontal pixel packing
packedColors = []
counter = 0
colorToCount = ""
numbersToSkip = 0

f.write("class " + fileName + "Class:\r") 
f.write("\tdef __init__(self):\r") 

# Amount of packed pixels will be stored in the first hex and color to use will be stored in the second value
f.write("\t\tself.HexArray = array.array('BB',") 

maxIndex = len(allColorsAsInt)

# Pack the colors
for index, color in enumerate(allColorsAsInt):

	if numbersToSkip != 0:
		numbersToSkip = numbersToSkip - 1
		continue

	if counter == 0:
		colorToCount = color
		while (index+counter < maxIndex and allColorsAsInt[index+counter] == colorToCount):
			counter = counter + 1
		packedColors.append([int(counter),int(color)])
		numbersToSkip = counter -1
		counter = 0

#print(packedColors)
#print(len(packedColors))

lastHexColorIndex = len(packedColors) - 1

base = b''

# Generate packed colors in hex format. As we use 1 byte for the first hex value, packed pixel amounts over 255 will be split into consequtive
for index, color in enumerate(packedColors):
	indexLeft = packedColors[index][0]
	while indexLeft >= 255:
		tempHex = pack('BB', 255, packedColors[index][1])
		indexLeft -= 255
		base += tempHex
	tempHex = pack('BB', indexLeft, packedColors[index][1])	
	base += tempHex

# Print the output hex
f.write(str(base))
#print(base)

f.write(")\r")

# Write image name
f.write("\t\tself.ImageName = \"" + str(fileName) + "\"\r")

# Write image width
f.write("\t\tself.ImageWidth = " + str(w) + "\r")

# Write image height
f.write("\t\tself.ImageHeight = " + str(h) + "\r")

# Write total pixel count
f.write("\t\tself.ImagePixelCount = " + str(w*h) + "\r")

# Write the amount of packed coloring actions in the hex array
f.write("\t\tself.ImagePackedColorCount = " + str(len(packedColors)) + "\r")

# Write the amount of different colors used in the image
f.write("\t\tself.ColorAmount = " + str(len(hexColors)) + "\r")

# Count how many pixels use each unique hex color
colorCounts = []
for color in hexColors:
	colorCounts.append(allColors.count(color))

# Write each color with RGBA values, hex format and how many times it's used
for index, color in enumerate(hexColors):

	# Parse a bit 0x000000ff -> 000000ff
	tempHex = str(color)[3:-1]

	r,g,b,a = bytes.fromhex(tempHex)

	f.write("\t\tself.Color" + str(index) + " = (" + str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a) + ") # " + color +". Times used: " + str(colorCounts[index])+ " \r")


# Write an int list of all used colors
f.write("\t\tself.ColorList = [")

lastIndex = len(hexColors) - 1

for index, color in enumerate(hexColors):
	if index != lastIndex:
		f.write("self.Color" + str(index) + ", ")
	else:
		f.write("self.Color" + str(index))

f.write("]")

f.close()

print("Done")
