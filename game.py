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

    def mixItems(self):
        for item in self.recipe:
            self.canvas.data[item] = ""
        self.response = "Yum cookie dough."
        self.canvas.data["bowl"] = PhotoImage(file="bowl_mixed.gif")

    def transferToSheet(self):
        if self.scooped:
            self.response = "You scoop balls of cookie dough onto the baking sheet."
            self.canvas.data["sheet"] = PhotoImage(file="sheet_scooped.gif")
        else:
            self.response = "You put all of the dough onto the baking sheet."
            self.canvas.data["sheet"] = PhotoImage(file="sheet_giant_cookie.gif")


    def bakeCookies(self):
        if self.preheated:
            self.cookieTimer += 1
            self.canvas.data["oven"] = PhotoImage(file="oven_baking.gif")
            # self.canvas.data["sheet"] = ""
        else:
            self.response = "You didn't wait for the oven to heat up."
            self.gameOver("preheat")

    def putDownItem(self, command):
        if "bowl" not in command and self.item:
            if "egg" not in self.item:
                self.canvas.data[self.item] = PhotoImage(file=self.item+".gif")
                self.response = "You put the " + self.item + " back on the counter."
            else:
                self.eggsLeft += 1
                self.canvas.data[self.item] = PhotoImage(file=self.item + ".gif")
                self.response = "You put the egg back on the counter."
            self.item = ""
        elif "spoon" in command and "bowl" in command and self.item == "spoon":
            self.response = "You can't put the spoon in the bowl."

        elif "bowl" in command and self.item:
            if self.item == "milk":
                self.response = "I guess you can't read... there was no milk in the recipe!!!!!!!!"
                self.gameOver("milk")
                return
            elif self.item == "egg1":
                self.response = "Really? There were only two eggs in the recipe."
                self.gameOver("egg")
                return
            self.bowl += [self.item]
            self.canvas.data[self.item] = PhotoImage(file=self.item+"_bowl" + ".gif")
            if "egg" in self.item:
                self.response = "You add the egg to the bowl."
            else:
                self.response = "You add the " + self.item + " to the bowl."
            self.item = ""
        elif "oven" in command:
            if self.scooped:
                self.bakeCookies()
            else:
                self.gameOver("bowl")

        else:
            self.response = "You aren't carrying anything!"
        return

    def pickUpItem(self, command):
        if self.item and self.item in command:
            self.response = "You already have that item."
            return

        if self.item:
            self.response = "You can't pick up that many things at once!"
            return

        for item in self.bowl:
            if item in command:
                self.response = "You already used all of the " + item + "."
                return
            elif "egg" in command and "egg1" in self.bowl and not self.eggsLeft:
                self.response = "There are no more eggs!"
                return

        if "sugar" in command:
            self.item = "sugar"

        elif "chocolate" in command:
            self.item = "chocolate"

        elif "milk" in command:
            self.item = "milk"

        elif "flour" in command:
            self.item = "flour"

        elif "butter" in command:
            self.item = "butter"

        elif "egg" in command and self.eggsLeft != 0:
            self.item = "egg" + str(self.eggsLeft)
            self.canvas.data[self.item] = ""
            self.eggsLeft -= 1
            self.response = "You picked up an egg."
            return

        elif "spoon" in command:
            self.item = "spoon"
            self.canvas.data["spoon"] = ""
            self.response = "Ready to mix."
            return

        elif "book" in command:
            self.response = "Why don't you just read it?"
            return

        elif "bowl" in command:
            self.response = "What are you trying to do with the bowl?"
            return

        else:
            self.response = "I did not understand your request."
            return

        self.canvas.data[self.item] = ""
        self.response = "You picked up the " + self.item + "."
        return

    def runCommand(self, command):
        self.keyText = ""
        if self.macaron:
            if command == "continue":
                self.macaron += 1
                if self.macaron - 2 == len(self.macaronText):
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
        elif ("sheet" in command or "tray" in command or "pan" in command) and "dough" in command:
            if self.mixed:
                self.scooped = "spoon" in command or "scoop" in command
                self.transferToSheet()
            else:
                self.response = "I don't think you're ready for that yet."
        elif "cookie" in command or "recipe" in command:
            if self.bookOpened:
                self.response = "Ingredients: flour, sugar, 2 eggs, 1 stick of butter, chocolate chips\n" \
                                "Preheat oven to 350 degrees F. Mix together all of the ingredients.\n" \
                                "Spoon dough onto a baking sheet. Bake for 10-30 minutes. Let cool before eating. :)"
            else:
                self.response = "Open the book first."
        elif "pick" in command or "get" in command:
            self.pickUpItem(command)

        elif "oven" in command and "in" in command:
            print "ok"
        elif "place" in command or "put" in command or "down" in command:
            self.putDownItem(command)
        elif "mix" in command:
            if self.item == "spoon":
                if set(self.recipe) == set(self.bowl):
                    self.mixed = True
                    self.mixItems()
                else:
                    self.gameOver("ingredients")
            else:
                self.response = "Are you trying to mix this with your hands? Gross."
        else:
            self.response = "I don't know how to " + command + "."


        self.redrawAll()

    def onTimerFired(self):
        self.timerCounter += 1
        self.timerText = "timerCounter = " + str(self.timerCounter)
        if self.ovenTimer:
            self.ovenTimer += 1
            if self.ovenTimer == 55:
                self.gameOver("Fire")
            elif self.ovenTimer == 20:
                self.response = "The oven is ready to go."
                self.preheated = True
                self.canvas.data["oven"] = PhotoImage(file="preheated_oven.gif")
        if self.cookieTimer:
            self.cookieTimer += 1
            if self.cookieTimer == 11:
                self.canvas.data["oven"] = PhotoImage(file="oven_cooked.gif")
            elif self.cookieTimer == 31:
                self.canvas.data["oven"] = PhotoImage(file="oven_burnt.gif")
                self.gameOver("burnt")
        if self.minute == 59:
            self.hour += 1
            self.minute = 0
        else:
            self.minute += 1
        if (self.timerCounter > 500) and self.win != True:
            self.gameOver("time")

    def redrawAll(self):
        self.canvas.delete(ALL)
        # draw the text
        self.canvas.create_rectangle(0,0, 999,999, fill = "#9ad413")
        self.canvas.create_rectangle(0, 780, 999, 999, fill = "#4d3f73")
        self.canvas.create_image(500, 500, image=self.canvas.data["clock"])
        self.canvas.create_image(500, 500, image=self.canvas.data["oven"])
        self.canvas.create_image(500, 500, image=self.canvas.data["girl"])
        self.canvas.create_image(500, 500, image=self.canvas.data["counter"])
        self.canvas.create_image(500, 500, image=self.canvas.data["bowl"])
        self.canvas.create_image(500, 500, image=self.canvas.data["book"])
        self.canvas.create_image(500, 500, image=self.canvas.data["sheet"])
        self.canvas.create_image(500, 500, image=self.canvas.data["milk"])
        self.canvas.create_image(500, 500, image=self.canvas.data["egg3"])
        self.canvas.create_image(500, 500, image=self.canvas.data["egg2"])
        self.canvas.create_image(500, 500, image=self.canvas.data["egg1"])
        self.canvas.create_image(500, 500, image=self.canvas.data["flour"])
        self.canvas.create_image(500, 500, image=self.canvas.data["sugar"])
        self.canvas.create_image(500, 500, image=self.canvas.data["butter"])
        self.canvas.create_image(500, 500, image=self.canvas.data["chocolate"])
        self.canvas.create_image(500, 500, image=self.canvas.data["spoon"])
        self.canvas.create_image(500, 500, image=self.canvas.data["fire"])
        self.canvas.create_rectangle(0, 840, 999, 999, fill = "black")

        entered_text = self.canvas.create_text(20,968,text=self.carat + self.keyText, fill="white", anchor=W, font=('Helvetica', 20))
        self.canvas.create_text(20,860,text=self.response, fill="white", anchor=NW, font=('Helvetica', 20))

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
        self.cookieTimer = 0
        self.root = Tk()
        self.bowl = []
        self.recipe = ["butter", "chocolate", "egg2", "egg3", "flour", "sugar"]
        self.eggsLeft = 3
        self.preheated = False
        self.timerDelay = 250 # in milliseconds (set to None to turn off timer)
        self.canvas = Canvas(self.root, width=1000, height=1000)
        self.mixed = False
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
            "sheet": PhotoImage(file="sheet.gif"),
            "spoon": PhotoImage(file="spoon.gif"),
            "sugar": PhotoImage(file="sugar.gif")
        }
        self.response = "Let's bake some cookies!"
        self.keyText = ""
        self.item = ""
        self.minute = 0
        self.hour = 12
        self.carat = "> "
        self.ovenTimer = 0
        self.validSyms = ["space"] + [chr(x) for x in range(48, 58)] + [chr(x) for x in range(97, 123)]
        self.bookOpened = False
        self.scooped = False
        self.macaron = 0
        self.macaronText = [
            "How to make macarons:",
            "Preheat the oven to 300 degrees F using the convection setting.",
            "Line 3 baking sheets with silicone mats.",
            "Measure the confectioners' sugar and almond flour by spooning them into measuring cups and leveling with \n a knife.",
            "Transfer to a bowl; whisk to combine to combine.",
            "Sift the sugar-almond flour mixture, a little at a time, through a fine-mesh sieve into a large bowl, pressing \n with a rubber spatula to pass through as must as possible.",
            "It will take a while, and up to 2 tablespoons of coarse almond flour may be left; just toss it.",
            "Beat the egg whites, cream of tartar and salt with a mixer on medium speed until frothy.",
            "Increase the speed to medium high; gradually add the superfine sugar and beat until stiff and shiny, about 5 \n more minutes.",
            "Transfer the batter to a pastry bag fitted with a 1/4-inch round tip.",
            "Holding the bag vertically and close to the baking sheet, pipe 1 1/4-inch circles (24 per sheet).",
            "Firmly tap the backing sheets twice against the counter to release any air bubbles.",
            "Let the cookies sit at room temperature until the tops are no longer sticky to the touch, 15 minutes to 1 hour, \n depending on the humidity.",
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
        elif string == "Macaron":
            self.response = "You spent all day reading the macaron recipe..."
        elif string == "time":
            self.response = "You wasted all your time... how are you so slow?"
        self.redrawAll()
        # time.sleep(10)
        self.response = "Play again? Type 'yes' to restart."

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
