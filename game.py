# eventBasedAnimationDemo.py

from Tkinter import *
import math

# eventBasedAnimationClass.py

import sys

class EventBasedAnimationClass(object):
    def onMousePressed(self, event):
        self.mouseText = "last mousePressed: " + str((event.x, event.y))

    def validKey(self, key):
        return (key in self.validSyms)

    def onKeyPressed(self, event):
        if self.validKey(event.keysym):
            self.keyText += (event.char)
        elif event.keysym == "Return" and len(self.keyText):
            self.runCommand(self.keyText)
        elif event.keysym == "BackSpace" and len(self.keyText):
            self.keyText = self.keyText[:-1]

    def runCommand(self, command):
        self.response = "I don't know how to " + command + "."
        self.keyText = ""
        self.redrawAll()

    def onTimerFired(self):
        self.timerCounter += 1
        self.timerText = "timerCounter = " + str(self.timerCounter)

        if (self.minute == 59):
            self.hour += 1
            self.minute = 0
        else:
            self.minute += 1
        if (self.timerCounter > 180) and self.win != True:
            print "ure a loser"
            # self.gameOver()
        self.updateClock()

    def redrawAll(self):
        self.canvas.delete(ALL)
        # draw the text
        self.canvas.create_image(500, 500, image=self.canvas.data['image'])
        self.canvas.create_rectangle(0, 840, 999, 999, fill = "black")

        self.canvas.create_text(150,20,text="events-example1.py")
        entered_text = self.canvas.create_text(20,968,text=self.carat + self.keyText, fill="white", anchor=W, font=('Helvetica', 20))
        self.canvas.create_text(20,860,text=self.response, fill="white", anchor=W, font=('Helvetica', 20))

        x0 = self.canvas.bbox(entered_text)[0]
        x1 = self.canvas.bbox(entered_text)[2]

        self.canvas.create_text(150,80,text=self.timerText)
        self.canvas.create_text(150,40,text=self.mouseText)

        if self.timerCounter % 4 == 1 or self.timerCounter % 4 == 0:
            self.canvas.create_line(20+x1-x0, 955, 20+x1-x0, 980, fill="white")
        self.updateClock()



    def updateClock(self):
        width = (583 - 440)
        height = (196 - 45)
        r = min(width, height)/2
        cx = (440 + 583)/2
        cy = (45 + 196)/2

        # adjust the hour to take the minutes into account
        hour = self.hour
        hour += self.minute/60.0

        # find the hourAngle and draw the hour hand
        # but we must adjust because 0 is vertical and
        # it proceeds clockwise, not counter-clockwise!
        hourAngle = math.pi/2 - 2*math.pi*hour/12
        hourRadius = r*1/2
        hourX = int(round(cx + hourRadius * math.cos(hourAngle)))
        hourY = int(round(cy - hourRadius * math.sin(hourAngle)))
        self.canvas.create_line(cx, cy, hourX, hourY, fill="black", width=1)

        # repeat with the minuteAngle for the minuteHand
        minuteAngle = math.pi/2 - 2*math.pi*self.minute/60
        minuteRadius = r*9/10
        minuteX = cx + minuteRadius * math.cos(minuteAngle)
        minuteY = cy - minuteRadius * math.sin(minuteAngle)
        self.canvas.create_line(cx, cy, minuteX, minuteY, fill="black", width=1)

    def initAnimation(self):
        self.mouseText = "No mousePresses yet"
        self.keyText = ""
        self.timerText = "No timerFired calls yet"
        self.timerCounter = 0

    def __init__(self, width=1000, height=1000):
        self.width = width
        self.win = False
        self.timerCounter = 0
        self.root = Tk()
        self.height = height
        self.text = ""
        self.timerDelay = 250 # in milliseconds (set to None to turn off timer)
        self.canvas = Canvas(self.root, width=1000, height=1000)
        image = PhotoImage(file="1.gif")
        self.canvas.data = {}
        self.canvas.data["image"] = image
        self.mouseText = "hello"
        self.keyText = ""
        self.timerText = "no time"
        self.minute = 0
        self.hour = 12
        self.carat = "> "
        self.response = "Let's bake some cookies!"
        self.validSyms = ["Space"] + [chr(x) for x in range(48, 58)] + [chr(x) for x in range(65, 91)] + [chr(x) for x in range(97, 123)]
        self.redrawAll()

    def onMousePressedWrapper(self, event):
        if (not self._isRunning): return
        self.onMousePressed(event)
        self.redrawAll()

    def onKeyPressedWrapper(self, event):
        if (not self._isRunning): return
        self.onKeyPressed(event)
        self.redrawAll()

    def onTimerFiredWrapper(self):
        if (not self._isRunning): self.root.destroy(); return
        if (self.timerDelay == None): return # turns off timer
        self.onTimerFired()

        self.redrawAll()
        self.canvas.after(self.timerDelay, self.onTimerFiredWrapper)

    def quit(self):
        if (not self._isRunning): return
        self._isRunning = False
        if (self.runningInIDLE):
            # in IDLE, must be sure to destroy here and now
            self.root.destroy()
        else:
            # not IDLE, then we'll destroy in the canvas.after handler
            self.root.quit()

    def run(self):
        # create the root and the canvas
        self.canvas.pack()

        # self.init(self.canvas)
        self.initAnimation()
        # set up events
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit())
        self._isRunning = True
        self.runningInIDLE =  ("idlelib" in sys.modules)
        # DK: You can use a local function with a closure
        # to store the canvas binding, like this:
        def f(event): self.onMousePressedWrapper(event)
        self.root.bind("<Button-1>", f)
        # DK: Or you can just use an anonymous lamdba function, like this:
        self.root.bind("<Key>", lambda event: self.onKeyPressedWrapper(event))
        self.onTimerFiredWrapper()
        # and launch the app (This call BLOCKS, so your program waits
        # until you close the window!)
        self.root.mainloop()

EventBasedAnimationClass().run()
