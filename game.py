from Tkinter import *
import math
import time
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
        elif event.keysym == "BackSpace":
            self.keyText = self.keyText[:-1]

    def runCommand(self, command):
        self.response = "I don't know how to " + command + "."
        self.keyText = ""
        if self.macaron:
            if command == "continue":
                self.macaron += 1
                if self.macaron == len(self.macaronText) - 2:
                    self.gameOver("Macaron")
                else:
                    self.response = self.macaronText[self.macaron - 2]
            else:
                self.response = "Type 'continue' to keep reading."
        elif "preheat" in command or "heat" in command or ("turn on" in command and "oven" in command):
            self.response = "The oven is heating up."
            self.canvas.data["oven"] = PhotoImage(file="preheating_oven.gif")
            self.ovenTimer = 1
        elif "book" in command:
            if self.bookOpened:
                if "read" in command:
                    self.response = "You opened the book to a recipe to make macarons. Type 'continue' to keep reading."
                    self.macaron = 1
            else:
                if "read" in command:
                    self.response = "It says 'Cookbook'."
                elif "open" in command:
                    self.response = "You open the book."
                    self.bookOpened = True
        elif "cookie" in command and "recipe" in command:
            if self.bookOpened:
                self.response = "Ingredients: \u00B7\t flour, sugar, 2 eggs, 1 stick of butter, chocolate chips\n" \
                                "Preheat oven to 350 degrees F. Mix together all of the ingredients.\n" \
                                "Spoon dough onto a baking sheet. Bake for 10-30 minutes. Let cool before eating. :)"
            else:
                self.response = "Open the book first."

        self.redrawAll()

    def onTimerFired(self):
        self.timerCounter += 1
        self.timerText = "timerCounter = " + str(self.timerCounter)
        if self.ovenTimer:
            self.ovenTimer += 1
            if self.ovenTimer == 55:
                self.gameOver("Fire")
            elif self.ovenTimer == 20:
                self.response = "The  is ready to go."
                self.canvas.data["oven"] = PhotoImage(file="preheated_oven.gif")
        if self.minute == 59:
            self.hour += 1
            self.minute = 0
        else:
            self.minute += 1
        if (self.timerCounter > 300) and self.win != True:
            print "ure a loser"
            # self.gameOver()

    def redrawAll(self):
        self.canvas.delete(ALL)
        # draw the text
        self.canvas.create_rectangle(0,0, 999,999, fill = "#9ad413")
        self.canvas.create_rectangle(0, 780, 999, 999, fill = "#4d3f73")
        self.canvas.create_image(500, 500, image=self.canvas.data["clock"])
        self.canvas.create_image(500, 500, image=self.canvas.data["oven"])
        self.canvas.create_image(500, 500, image=self.canvas.data["girl"])
        self.canvas.create_image(500, 500, image=self.canvas.data["counter"])
        self.canvas.create_image(500, 500, image=self.canvas.data["milk"])
        self.canvas.create_image(500, 500, image=self.canvas.data["egg3"])
        self.canvas.create_image(500, 500, image=self.canvas.data["egg2"])
        self.canvas.create_image(500, 500, image=self.canvas.data["egg1"])
        self.canvas.create_image(500, 500, image=self.canvas.data["flour"])
        self.canvas.create_image(500, 500, image=self.canvas.data["sugar"])
        self.canvas.create_image(500, 500, image=self.canvas.data["butter"])
        self.canvas.create_image(500, 500, image=self.canvas.data["chocolate"])
        self.canvas.create_image(500, 500, image=self.canvas.data["bowl"])
        self.canvas.create_image(500, 500, image=self.canvas.data["spoon"])
        self.canvas.create_image(500, 500, image=self.canvas.data["book"])
        self.canvas.create_image(500, 500, image=self.canvas.data["fire"])
        self.canvas.create_rectangle(0, 840, 999, 999, fill = "black")

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
        self.height = height
        self.win = False
        self.timerCounter = 0
        self.root = Tk()
        self.timerDelay = 250 # in milliseconds (set to None to turn off timer)
        self.canvas = Canvas(self.root, width=1000, height=1000)
        self.canvas.data = {
            "oven": PhotoImage(file="base_oven.gif"),
            "fire": "",
            "clock": PhotoImage(file="clock.gif"),
            "book": PhotoImage(file="book_counter.gif"),
            "bowl": PhotoImage(file="bowl.gif"),
            "butter": PhotoImage(file="butter.gif"),
            "chocolate": PhotoImage(file="chocolate.gif"),
            "counter": PhotoImage(file="counter.gif"),
            "egg1": PhotoImage(file="egg1.gif"),
            "egg2": PhotoImage(file="egg2.gif"),
            "egg3": PhotoImage(file="egg3.gif"),
            "flour": PhotoImage(file="flour.gif"),
            "girl": PhotoImage(file="girl.gif"),
            "milk": PhotoImage(file="milk.gif"),
            "spoon": PhotoImage(file="spoon.gif"),
            "sugar": PhotoImage(file="sugar.gif")
        }
        self.response = "Let's bake some cookies!"
        self.keyText = ""
        self.minute = 0
        self.hour = 12
        self.carat = "> "
        self.ovenTimer = 0
        self.validSyms = ["space"] + [chr(x) for x in range(48, 58)] + [chr(x) for x in range(97, 123)]
        self.bookOpened = False
        self.macaron = 0
        self.macaronText = [
            "How to make macarons:"
            "Preheat the oven to 300 degrees F using the convection setting.",
            "Line 3 baking sheets with silicone mats.",
            "Measure the confectioners' sugar and almond flour by spooning them into measuring cups and leveling with a knife.",
            "Transfer to a bowl; whisk to combine to combine.",
            "Sift the sugar-almond flour mixture, a little at a time, through a fine-mesh sieve into a large bowl, pressing with a rubber spatula to pass through as must as possible.",
            "It will take a while, and up to 2 tablespoons of coarse almond flour may be left; just toss it.",
            "Beat the egg whites, cream of tartar and salt with a mixer on medium speed until frothy.",
            "Increase the speed to medium high; gradually add the superfine sugar and beat until stiff and shiny, about 5 more minutes.",
            "Transfer the batter to a pastry bag fitted with a 1/4-inch round tip.",
            "Holding the bag vertically and close to the baking sheet, pipe 1 1/4-inch circles (24 per sheet).",
            "Firmly tap the backing sheets twice against the counter to release any air bubbles.",
            "Let the cookies sit at room temperature until the tops are no longer sticky to the touch, 15 minutes to 1 hour, depending on the humidity.",
            "Slip another baking sheet under the first batch (a double baking sheet protects the cookies from the heat).",
            "Bake the first batch until the cookies are shiny and rise 1/8 inch to form a 'foot,' about 20 minutes.",
            "Transfer to a rack to cool completely.",
            "Peel the cookies off the mats and sandwich a thin layer of filling."
        ]

        self.mouseText = "hello"
        self.timerText = "no time"

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

    def gameOver(self, string):
        if string == "Fire":
            self.canvas.data["fire"] = PhotoImage(file="fire.gif")
            self.response = "You set the house on fire..."
            self.redrawAll()
            time.sleep(10)
        elif string == "Macaron":
            self.response = "You spent all day reading the macaron recipe..."
            self.redrawAll()
            time.sleep(10)
        self.response = "Play again? Type 'Yes' to restart."
        self.redrawAll()

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
