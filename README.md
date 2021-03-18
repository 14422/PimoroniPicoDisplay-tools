# PimoroniPicoDisplay-tools
Features my python image converter, which turns an input image into 2 byte hex array (without resolution or color modifications) and micropython code for drawing it
---
How to use?
---
* ImageConverter.py
1. With some tool of your choice, create a suitable picture for the Pico display (240x135 at max) with 128 colors for example. I'm using Aseprite myself.
2. Run the ImageConverter.py with the image as parameter. For example 'Python ImageConverter.py botw128.png'. Output will be a python file with the image's name. botw128.py in my case
3. Upload your image to Pico. I'm using Thonny with Windows.

---


* ImageDrawingDemo.py
1. Import the image you uploaded to Pico and create a new object of it. A ready made class can be found within the python file

2. Call the method DrawPackedimage with the image as a parameter and wanted X, Y coordinates.
---
Example of output python file containing all the needed data for drawing. A picture with 8 colors in this case:

    import array

    class Botw8Class:

	  def __init__(self):  
  
		self.HexArray = array.array('BB',b'\x11\x05\x01\x06\'\x05\x03\x06\x04\x05B\x06....    
		self.ImageName = "Botw8"
		self.ImageWidth = 240
		self.ImageHeight = 135
		self.ImagePixelCount = 32400
		self.ImagePackedColorCount = 5257
		self.ColorAmount = 8
		self.Color0 = (65, 68, 32, 255) # (0x414420ff). Times used: 1450 
		self.Color1 = (106, 93, 49, 255) # (0x6a5d31ff). Times used: 1037 
		self.Color2 = (123, 113, 65, 255) # (0x7b7141ff). Times used: 1061 
		self.Color3 = (139, 137, 106, 255) # (0x8b896aff). Times used: 2857 
		self.Color4 = (148, 145, 115, 255) # (0x949173ff). Times used: 3961 
		self.Color5 = (164, 157, 123, 255) # (0xa49d7bff). Times used: 7203 
		self.Color6 = (205, 182, 131, 255) # (0xcdb683ff). Times used: 5842 
		self.Color7 = (246, 230, 180, 255) # (0xf6e6b4ff). Times used: 8989 
		self.ColorList = [self.Color0, self.Color1, self.Color2, self.Color3, self.Color4, self.Color5, self.Color6, self.Color7]
 
