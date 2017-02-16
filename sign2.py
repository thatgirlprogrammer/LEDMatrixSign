#!/usr/bin/python

# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

import time
from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics

maxHeight = 32

class displayElement:
    element = None
    delay = 0

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
            print 'run'
            self.readFile()
            double_buffer = self.matrix.CreateFrameCanvas()
            xpos = 0
            
            # main loop
            while True:
                for de in self.dispElemList:
                    #print type(de.element)
                    if isinstance(de.element, str):
                        self.ScrollText(de.element, de.delay, double_buffer)
                    elif isinstance(de.element, Image.Image):
                        self.ScrollImage(de.element, de.delay, double_buffer)
                    elif isinstance(de.element, Animation):
                        self.DisplayAnimation(de.element, double_buffer)

    def ScrollImage(self, img, delay, canvas):
        for n in range(canvas.width, -img.size[0], -1):
            canvas.Clear()
            #print 'SetImage: ', n, 0
            canvas.SetImage(img, n, 0)
            canvas = self.matrix.SwapOnVSync(canvas)
            if n == 0:
                time.sleep(float(delay))
            else:
                time.sleep(0.025)

                 

    def ScrollText(self, msg, delay, canvas):
        font = graphics.Font()
        font.LoadFont("../../fonts/10x20.bdf")
        textColor = graphics.Color(255, 0, 0)
        pos = canvas.width
        
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, 20, textColor, msg)
        
        for n in range(canvas.width, -len, -1):
            canvas.Clear()
            len = graphics.DrawText(canvas, font, n, 20, textColor, msg)
            
            canvas = self.matrix.SwapOnVSync(canvas)
            if n == 0:
                time.sleep(float(delay))
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
        f = open(self.file, "r")
        for line in f.readlines():
            v = line.split(",")
            print v
            value = v[1].rstrip()
            de = displayElement()
            de.delay = v[2]
            #print value
            if v[0] == "file":
                img  = Image.open(value).convert('RGB')
                img.load()
                img  = Scale(img)
                de.element = img
                self.dispElemList.append(de)
            elif v[0] == "text":
                de.element = value
                self.dispElemList.append(de)
            
            elif v[0] == "anim":
                a =self. readAnimation(value)
                de.element = a
                self.dispElemList.append(de)
    
        f.close()
            
        

def Scale(img):
        hpercent = (maxHeight/float(img.size[1]))
        width = int((float(img.size[0])*float(hpercent)))
        img = img.resize((width,maxHeight), Image.ANTIALIAS)
        #print img.size
        return img
        
#MAIN

if __name__ == "__main__":
    sign_scroller = signScrolling()
    if (not sign_scroller.process()):
        sign_scroller.print_help()
