'''
Tkinter GUI implementation of decimal clock
See https://en.wikipedia.org/wiki/Decimal_time
'''
import time
import tkinter as tkr
import tkinter.font as tkf
from collections import namedtuple
import datetime as dtt
import deciclock.decitime as dcc

def get_decimal_time() -> dcc.DecimalTime:
    '''Get local time as decimal'''
    now = dtt.datetime.now()
    return dcc.DecimalTime.from_conventional(now.time())

class ClockFace:
    '''Displays clock face and current time as an arc and in numerical form'''

    Options=namedtuple('Options', 'enable_emoji show_seconds show_symbols')
    Size=namedtuple('Size', 'radius padding')
    Colors=namedtuple('Colors', 'tick hour time noon midnight')

    def __init__(
            self, font_family, options, size, colors):
        self.canvas=tkr.Canvas(height=size.padding*2+size.radius*2
                               , width=size.padding*2+size.radius*2)
        self.canvas.pack(anchor=tkr.CENTER, expand=True)
        self.symbol_font=tkf.Font(family=font_family, size=48)
        self.time_font=tkf.Font(family=font_family, size=36, weight="bold")
        self.options=options
        self.size=size
        self.colors=colors

    def update(self):
        '''Update clock face and time'''
        self.canvas.delete('all')
        self.draw_scale()
        self.show_time()

    def draw_scale(self):
        '''Draw clock scale'''
        self.canvas.create_oval(
            self.size.padding, self.size.padding, self.size.radius*2+self.size.padding
            , self.size.radius*2+self.size.padding, width=1, outline=self.colors.tick)
        self.canvas.create_text(
            self.size.padding+self.size.radius, self.size.padding/2
            , justify=tkr.CENTER, anchor=tkr.CENTER
            , text=chr(127774) if self.options.enable_emoji else 'Noon'
            , fill=self.colors.noon, font=self.symbol_font)
        self.canvas.create_text(
            self.size.padding+self.size.radius, self.size.padding*1.5+self.size.radius*2
            , justify=tkr.CENTER, anchor=tkr.CENTER
            , text=chr(127771) if self.options.enable_emoji else 'Midnight'
            , fill=self.colors.midnight, font=self.symbol_font)

    def show_time(self):
        '''Show current time'''
        decitime=get_decimal_time()
        angle=decitime.ratio()*360
        self.canvas.create_arc(
            self.size.padding, self.size.padding
            , self.size.radius*2+self.size.padding, self.size.radius*2+self.size.padding
            , style=tkr.ARC, start=270, extent=-angle
            , width=10, outline=self.colors.hour)
        self.canvas.create_arc(
            self.size.padding, self.size.padding
            , self.size.radius*2+self.size.padding, self.size.radius*2+self.size.padding
            , style=tkr.PIESLICE, start=270-angle, extent=3, outline=''
            , fill=self.colors.hour)
        if self.options.show_seconds:
            text_format="{:02d}{}{:02d}{}{:02d}{}"
        else:
            text_format="{:02d}{}{:02d}{}"
        text = text_format.format(
            decitime.dhour, 'h' if self.options.show_symbols else ''
            , decitime.dminute, 'm' if self.options.show_symbols else ''
            , int(decitime.dsecond), 's' if self.options.show_symbols else '')
        self.canvas.create_text(
            self.size.padding+self.size.radius, self.size.padding+self.size.radius
            , justify=tkr.CENTER, text=text, fill=self.colors.time
            , font=self.time_font)

def run():
    root = tkr.Tk()
    root.geometry('600x600')
    root.title('Decimal Clock')

    clockFace = ClockFace(
        font_family="tkHeadingFont"
        , options=ClockFace.Options(enable_emoji=True, show_seconds=True, show_symbols=True)
        , size=ClockFace.Size(radius=150, padding=100)
        , colors=ClockFace.Colors(tick='dimgray', hour='springgreen', time='darkslategray'
        , noon='gold', midnight='midnightblue'))

    dtime=get_decimal_time()
    untilNextDsecond=1-(dtime.dsecond-int(dtime.dsecond))
    time.sleep(untilNextDsecond)

    def update():
        '''Update clock face each decimal second'''
        clockFace.update()
        root.after(int(dcc.DecimalTime.get_conventional_to_decimal_ratio()*1000), update)

    update()

    root.mainloop()
