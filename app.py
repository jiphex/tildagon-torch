import asyncio
import app

from events.input import Buttons, BUTTON_TYPES
from system.eventbus import eventbus
from system.patterndisplay.events import *
from tildagonos import tildagonos
import machine

class TorchApp(app.App):
    def set_leds(self):
        for n in range(13):
            print(n)
            tildagonos.leds[n] = (255,255,255)
        tildagonos.leds.write()

    def __init__(self):
        self.on = False
        print(machine.freq())
        self.old_freq = machine.freq()
        machine.freq(80000000) # clock down the cpu, its a torch
        eventbus.emit(PatternDisable())
        self.button_states = Buttons(self)
        self.set_leds()

    def update(self, delta):
        if not self.on:
            self.set_leds()
            self.on = True
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            self.button_states.clear()
         # Hold back to quit
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.back_time += delta / 1_000
        else:
            self.back_time = 0
        if self.back_time > 1:
            self.back_time = 0
            self.minimise()
            eventbus.emit(PatternEnable())
            machine.freq(self.old_freq)
            self.button_states.clear()
            for i in range(12):
                tildagonos.leds[i] = (0, 0, 0)

    def draw(self, ctx):
        ctx.save()
        ctx.gray(1.0).rectangle(-120,-120,240,240).fill()
        ctx.font_size = 20
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.gray(0.0).move_to(1,1).text("Hold reboop for 1s to exit")
        ctx.gray(0.6).move_to(1,25).text("v0.0.4")
        ctx.restore()

__app_export__ = TorchApp
