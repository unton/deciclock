#!/usr/bin/env python3

import time
import decitime as dcc
import datetime as dtt
import tkinter as tkr
import tkinter.font as tkf

def getDecimalTime() -> dcc.DecimalTime:
    now = dtt.datetime.now()
    return dcc.from_conventional(now.time())

class ClockFace(tkr.Canvas):
  def __init__(self, fontFamily, enableEmoji, showSeconds, showSymbols, radius, padding
               , tickColor, hourColor, timeColor, noonColor, midnightColor):
    super().__init__(height=padding*2+radius*2, width=padding*2+radius*2)
    self.symbolFont=tkf.Font(family=fontFamily, size=48)
    self.timeFont=tkf.Font(family=fontFamily, size=36, weight="bold")
    self.enableEmoji=enableEmoji
    self.showSeconds=showSeconds
    self.showSymbols=showSymbols
    self.radius=radius
    self.padding=padding
    self.hourColor=hourColor
    self.tickColor=tickColor
    self.timeColor=timeColor
    self.noonColor=noonColor
    self.midnightColor=midnightColor

  def update(self):
    super().delete('all')
    self.drawScale()
    self.showTime()

  def drawScale(self):
    super().create_oval(self.padding, self.padding, self.radius*2+self.padding, self.radius*2+self.padding, width=1, outline=self.tickColor)
    super().create_text(self.padding+self.radius, self.padding/2, justify=tkr.CENTER, anchor=tkr.CENTER
                        , text=chr(127774) if self.enableEmoji else 'Noon'
                        , fill=self.noonColor, font=self.symbolFont)
    super().create_text(self.padding+self.radius, self.padding*1.5+self.radius*2, justify=tkr.CENTER, anchor=tkr.CENTER
                        , text=chr(127771) if self.enableEmoji else 'Midnight'
                        , fill=self.midnightColor, font=self.symbolFont)

  def showTime(self):
    dtime=getDecimalTime()
    angle=dtime.ratio()*360
    super().create_arc(self.padding, self.padding, self.radius*2+self.padding, self.radius*2+self.padding
                       , style=tkr.ARC, start=270, extent=-angle, width=10, outline=self.hourColor) 
    super().create_arc(self.padding, self.padding, self.radius*2+self.padding, self.radius*2+self.padding
                       , style=tkr.PIESLICE, start=270-angle, extent=3, outline='', fill=self.hourColor) 
    textFormat="{:02d}{}{:02d}{}{:02d}{}" if self.showSeconds else "{:02d}{}{:02d}{}{:02d}{}"
    text = textFormat.format(dtime.dhour, 'h' if self.showSymbols else ''
                             , dtime.dminute, 'm' if self.showSymbols else ''
                             , int(dtime.dsecond), 's' if self.showSymbols else '')
    super().create_text(self.padding+self.radius, self.padding+self.radius, justify=tkr.CENTER
                        , text=text, fill=self.timeColor
                        , font=self.timeFont)

root = tkr.Tk()
root.geometry('600x600')
root.title('Decimal Clock')

clockFace = ClockFace(fontFamily="tkHeadingFont", enableEmoji=True, showSeconds=True, showSymbols=True
                      , radius=150, padding=100
                      , tickColor='dimgray', hourColor='springgreen', timeColor='darkslategray'
                      , noonColor='gold', midnightColor='midnightblue')
clockFace.pack(anchor=tkr.CENTER, expand=True)

dtime=getDecimalTime()
untilNextDsecond=1-(dtime.dsecond-int(dtime.dsecond))
time.sleep(untilNextDsecond)

def update():
  clockFace.update()
  root.after(int(dcc.DecimalTime._secondsRatio*1000), update)

update()

root.mainloop()
