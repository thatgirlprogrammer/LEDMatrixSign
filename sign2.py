#!/usr/bin/python

# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

import os
import time
import logging
from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics

maxHeight = 32
workingDir= "/home/pi/rpi-rgb-led-matrix/python/LEDMatrixSign"

class displayElement:
    element   = None
    inEffect  = ''
    Color     = None
    delay     = 0

class Animation:
    frames = []
    delay  = 0.0


class signScrolling(SampleBase):
    dispElemList = []
        
    def __init__(self, *args, **kwargs):
        super(signScrolling, self).__init__(*args, **kwargs)
        self.parser.add_argument("-f", "--file", help="The file to read", default="signContent.txt")

    def run(self):
        if not 'file' in self.__dict__:
            self.file = self.args.file
            logging.debug('run')
            
            os.chdir(workingDir)
            self.readFile()
            double_buffer = self.matrix.CreateFrameCanvas()
            
            # main loop
            try:
                while True:
                    #print 'loop'
                    for de in self.dispElemList:
                        #print type(de.element)
                        if isinstance(de.element, str):
                            #print 'string'
                            if de.inEffect == 'ScrollRL':
                                self.ScrollTextRL(de, double_buffer)
                            elif de.inEffect == 'ScrollUp':
                                self.ScrollTextUp(de, double_buffer)
                            elif de.inEffect == 'Display':
                                self.displayText(de, double_buffer)
                            else:
                                print 'unknown effect'
                        elif isinstance(de.element, Image.Image):
                            #print 'image'
                            if de.inEffect == 'ScrollRL':
                                self.ScrollImageRL(de, double_buffer)
                            elif de.inEffect == 'ScrollUp':
                                self.ScrollImageUp(de, double_buffer)
                            elif de.inEffect == 'Display':
                                self.DisplayImage(de, double_buffer)
                            else:
                                print 'unknown effect'
                        elif isinstance(de.element, Animation):
                            #print 'animation'
                            self.DisplayAnimation(de, double_buffer)
                        else:
                            print 'unknown type'
            except:
                print "shutting down"


    def ScrollImageRL(self, de, canvas):
        #print 'ScrollImageRL'
        center = canvas.width/2
        len = de.element.size[0]
        #print len
        delayPos = center - (len/2)
        for n in range(canvas.width, -(de.element.size[0] + 1), -1):
            canvas.Clear()
            #print 'SetImage: ', n, 0
            canvas.SetImage(de.element, n, 0)
            canvas = self.matrix.SwapOnVSync(canvas)
            if n == delayPos:
                time.sleep(float(de.delay))
            else:
                time.sleep(0.025)

    def ScrollImageUp(self, de, canvas):
        #print 'ScrollImageUp'
        center = canvas.width/2
        len = de.element.size[0]
        #print len
        pos = center - (len/2)

        for n in range(maxHeight, -1, -1):
            canvas.Clear()
            #print 'SetImage: ', n, 0
            canvas.SetImage(de.element, pos, n)
            canvas = self.matrix.SwapOnVSync(canvas)
            if n == 0:
                time.sleep(float(de.delay))
            else:
                time.sleep(0.025)

    def DisplayImage(self, de, canvas):
        #print 'DisplayImage'
        center = canvas.width/2
        len = de.element.size[0]
        #print len
        pos = center - (len/2)
        
        canvas.Clear()
        #print 'SetImage: ', n, 0
        canvas.SetImage(de.element, pos, 0)
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(float(de.delay))
        
    def displayText(self, de, canvas):
        font = graphics.Font()
        font.LoadFont("../../fonts/10x20.bdf")
        textColor = de.Color
        center = canvas.width/2
        len = graphics.DrawText(canvas, font, 0, 0, textColor, de.element)
        pos = center - (len/2)
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, 20, textColor, de.element)         
        canvas = self.matrix.SwapOnVSync(canvas)
        time.sleep(float(de.delay))

    def ScrollTextRL(self, de, canvas):
        #print 'ScrollText'
        font = graphics.Font()
        font.LoadFont("../../fonts/10x20.bdf")
        #print de.Color
        textColor = de.Color
        pos = canvas.width
        
        center = canvas.width/2
        len = graphics.DrawText(canvas, font, 0, 0, textColor, de.element)
        delayPos = center - (len/2)
        
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, 20, textColor, de.element)
        
        for n in range(canvas.width, -len, -1):
            canvas.Clear()
            len = graphics.DrawText(canvas, font, n, 20, textColor, de.element)
            
            canvas = self.matrix.SwapOnVSync(canvas)
            if n == delayPos:
                time.sleep(float(de.delay))
            else:
                time.sleep(0.025)
                
    def ScrollTextUp(self, de, canvas):
        #print 'ScrollText'
        font = graphics.Font()
        font.LoadFont("../../fonts/10x20.bdf")
        #print de.Color
        textColor = de.Color
        
        center = canvas.width/2
        len = graphics.DrawText(canvas, font, 0, 0, textColor, de.element)
        pos = center - (len/2)
        
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, maxHeight, textColor, de.element)
        
        #Make the loop go to -1 so that we scroll all the way off the screen.
        for n in range(maxHeight, -1, -1):
            canvas.Clear()
            len = graphics.DrawText(canvas, font, pos, n, textColor, de.element)
            
            canvas = self.matrix.SwapOnVSync(canvas)
            #pause at 20 becuase it is centered on the display with the font we are using
            if n == 20:
                time.sleep(float(de.delay))
            else:
                time.sleep(0.025)
        
    def readAnimation(self, filename):
        #print 'readAnimation: ', filename
            
        animation = Animation()
        
        im = Image.open(filename)
        im.load()
        try:
            while 1:
                #print 'read frame'
                a = im.copy().convert('RGB')
                a = Scale(a)
                animation.frames.append(a)
                im.seek(len(animation.frames)) # skip to next frame
        
        except EOFError:
            pass # we're done
            
        try:
            #print 'read duration'
            animation.delay = im.info['duration']
            #print 'read duration from gif'
            #print animation.delay
        except KeyError:
            animation.delay = 100
            #print 'defaulting duration'
            #print 'delay: ', animation.delay

        return animation
    
    def DisplayAnimation(self, anim, canvas):
        #print len(anim.frames)
        #print anim.delay/1000.0
        numberFrames = len(anim.frames)
        currentFrame = 0
        for n in range(canvas.width, -anim.frames[0].size[0], -1):
            #print 'display frame: ', currentFrame
            canvas.Clear()
            canvas.SetImage(anim.frames[currentFrame], n, 0)
            canvas = self.matrix.SwapOnVSync(canvas)
            s = anim.delay/1000.0
            #print 'sleep: ', s
            time.sleep(s)
            if currentFrame == (numberFrames - 1):
                currentFrame = 0
            else:
                currentFrame += 1


    def readFile(self):
        print 'file read: ', self.file
        f = open(self.file, "r")
        for line in f.readlines():
            try:
                if line[0] != '#':
                    v = line.split(",")
                    #print v
                    value = v[1].strip()
                    de = displayElement()
                    de.inEffect = v[2].strip()
                    r = int(v[3].strip())
                    g = int(v[4].strip())
                    b = int(v[5].strip())<<<<<<< HEAD
                    #print 'converting to color'
                    de.Color = graphics.Color(r, g, b)
                    #print de.Color
                    de.delay = v[6].strip()
                    #print value
                    if v[0].strip() == "file":
                        img  = Image.open(value).convert('RGB')
                        img.load()
                        img  = Scale(img)
                        de.element = img
                        self.dispElemList.append(de)
                    elif v[0].strip() == "text":
                        de.element = value
                        self.dispElemList.append(de)
                    elif v[0].strip() == "anim":
                        a =self. readAnimation(value)
                        de.element = a
                        self.dispElemList.append(de)
            except:
                    print 'error on line ', line

        f.close()
          
        

def Scale(img):
        hpercent = (maxHeight/float(img.size[1]))
        width = int((float(img.size[0])*float(hpercent)))
        img = img.resize((width,maxHeight), Image.ANTIALIAS)
        #print img.size
        return img
        
#MAIN

if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/LEDMatrixSign',level=logging.DEBUG)
    logging.info('LEDMatrixSign v1.0 starting')
    sign_scroller = signScrolling()
    if (not sign_scroller.process()):
        sign_scroller.print_help()
