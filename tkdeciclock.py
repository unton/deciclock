#!/usr/bin/env python3
'''
Tkinter GUI implementation of decimal clock
See https://en.wikipedia.org/wiki/Decimal_time
'''
import time
import tkinter as tkr
import tkinter.font as tkf
import datetime as dtt
import decitime as dcc

def get_decimal_time() -> dcc.DecimalTime:
    '''Get local time as decimal'''
    now = dtt.datetime.now()
    return dcc.DecimalTime.from_conventional(now.time())

class ClockFace(tkr.Canvas):
    '''Displays clock face and current time as an arc and in numerical form'''
    def __init__(
            self, font_family, enable_emoji, show_seconds, show_symbols
            , radius, padding
            , tick_color, hour_color, time_color, noon_color, midnight_color):
        super().__init__(height=padding*2+radius*2, width=padding*2+radius*2)
        self.symbol_font=tkf.Font(family=font_family, size=48)
        self.time_font=tkf.Font(family=font_family, size=36, weight="bold")
        self.enable_emoji=enable_emoji
        self.show_seconds=show_seconds
        self.show_symbols=show_symbols
        self.radius=radius
        self.padding=padding
        self.hour_color=hour_color
        self.tick_color=tick_color
        self.time_color=time_color
        self.noon_color=noon_color
        self.midnight_color=midnight_color

    def update(self):
        '''Update clock face and time'''
        super().delete('all')
        self.draw_scale()
        self.show_time()

    def draw_scale(self):
        '''Draw clock scale'''
        super().create_oval(
            self.padding, self.padding, self.radius*2+self.padding
            , self.radius*2+self.padding, width=1, outline=self.tick_color)
        super().create_text(
            self.padding+self.radius, self.padding/2
            , justify=tkr.CENTER, anchor=tkr.CENTER
            , text=chr(127774) if self.enable_emoji else 'Noon'
            , fill=self.noon_color, font=self.symbol_font)
        super().create_text(
            self.padding+self.radius, self.padding*1.5+self.radius*2
            , justify=tkr.CENTER, anchor=tkr.CENTER
            , text=chr(127771) if self.enable_emoji else 'Midnight'
            , fill=self.midnight_color, font=self.symbol_font)

    def show_time(self):
        '''Show current time'''
        decitime=get_decimal_time()
        angle=decitime.ratio()*360
        super().create_arc(
            self.padding, self.padding
            , self.radius*2+self.padding, self.radius*2+self.padding
            , style=tkr.ARC, start=270, extent=-angle
            , width=10, outline=self.hour_color)
        super().create_arc(
            self.padding, self.padding
            , self.radius*2+self.padding, self.radius*2+self.padding
            , style=tkr.PIESLICE, start=270-angle, extent=3, outline=''
            , fill=self.hour_color)
        if self.show_seconds:
            text_format="{:02d}{}{:02d}{}{:02d}{}"
        else:
            text_format="{:02d}{}{:02d}{}"
        text = text_format.format(
            decitime.dhour, 'h' if self.show_symbols else ''
            , decitime.dminute, 'm' if self.show_symbols else ''
            , int(decitime.dsecond), 's' if self.show_symbols else '')
        super().create_text(self.padding+self.radius, self.padding+self.radius
                            , justify=tkr.CENTER, text=text, fill=self.time_color
                            , font=self.time_font)

root = tkr.Tk()
root.geometry('600x600')
root.title('Decimal Clock')

clockFace = ClockFace(
    font_family="tkHeadingFont"
    , enable_emoji=True, show_seconds=True, show_symbols=True
    , radius=150, padding=100
    , tick_color='dimgray', hour_color='springgreen', time_color='darkslategray'
    , noon_color='gold', midnight_color='midnightblue')
clockFace.pack(anchor=tkr.CENTER, expand=True)

dtime=get_decimal_time()
untilNextDsecond=1-(dtime.dsecond-int(dtime.dsecond))
time.sleep(untilNextDsecond)

def update():
    '''Update clock face each decimal second'''
    clockFace.update()
    root.after(int(dcc.DecimalTime._secondsRatio*1000), update)

update()

root.mainloop()
