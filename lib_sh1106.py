#!/usr/bin/env python

import smbus
from PIL import Image, ImageDraw

class sh1106():
    """
    A device encapsulates the I2C connection (address/port) to the SH1106
    OLED display hardware. The init method pumps commands to the display
    to properly initialize it. Further control commands can then be
    called to affect the brightness. Direct use of the command() and
    data() methods are discouraged.
    """

    def __init__(self, bus, address=0x3C):
        self.cmd_mode = 0x00
        self.data_mode = 0x40
        self.bus = bus
        self.addr = address
        self.width = 128
        self.height = 64
        self.pages = int(self.height / 8)
        self.image = Image.new('1', (self.width, self.height))
        self.canvas = ImageDraw.Draw(self.image) # this is a "draw" object for preparing display contents
        
        self._command(
            const.DISPLAYOFF,
            const.MEMORYMODE,
            const.SETHIGHCOLUMN,      0xB0, 0xC8,
            const.SETLOWCOLUMN,       0x10, 0x40,
            const.SETCONTRAST,        0x7F,
            const.SETSEGMENTREMAP,
            const.NORMALDISPLAY,
            const.SETMULTIPLEX,       0x3F,
            const.DISPLAYALLON_RESUME,
            const.SETDISPLAYOFFSET,   0x00,
            const.SETDISPLAYCLOCKDIV, 0xF0,
            const.SETPRECHARGE,       0x22,
            const.SETCOMPINS,         0x12,
            const.SETVCOMDETECT,      0x20,
            const.CHARGEPUMP,         0x14,
            const.DISPLAYON)

    def _command(self, *cmd): 
        """
        Sends a command or sequence of commands through to the
        device - maximum allowed is 32 bytes in one go.
        """
        assert(len(cmd) <= 32)
        self.bus.write_i2c_block_data(self.addr, self.cmd_mode, list(cmd))

    def data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the
        device - maximum allowed in one transaction is 32 bytes, so if
        data is larger than this it is sent in chunks.
        """
        for i in range(0, len(data), 32):
            self.bus.write_i2c_block_data(self.addr,
                                          self.data_mode,
                                          list(data[i:i+32]))
    def display(self):
        """
        Takes a 1-bit image and dumps it to the SH1106 OLED display.
        """
        #assert(image.mode == '1')
        #assert(image.size[0] == self.width)
        # assert(image.size[1] == self.height)
        self._command(
            const.COLUMNADDR, 0x00, self.width - 1,
            const.PAGEADDR, 0x00, self.pages - 1)

        page = 0xB0
        pix = list(self.image.getdata())
        step = self.width * 8
        for y in range(0, self.pages * step, step):
            # move to given page, then reset the column address
            self._command(page, 0x02, 0x10)
            page += 1
            buf = []
            for x in range(self.width):
                byte = 0
                for n in range(0, step, self.width):
                    byte |= (pix[x + y + n] & 0x01) << 8
                    byte >>= 1
                buf.append(byte)
            self.data(buf)                  

    def cls(self):
        self.canvas.rectangle((0, 0, self.width-1, self.height-1), outline=0, fill=0)
        #self.display()

    def onoff(self, onoff):
        if onoff == 0:
            self._command(const.DISPLAYOFF)
        else:
            self._command(const.DISPLAYON)            

class const:
    CHARGEPUMP = 0x8D
    COLUMNADDR = 0x21
    COMSCANDEC = 0xC8
    COMSCANINC = 0xC0
    DISPLAYALLON = 0xA5
    DISPLAYALLON_RESUME = 0xA4
    DISPLAYOFF = 0xAE
    DISPLAYON = 0xAF
    EXTERNALVCC = 0x1
    INVERTDISPLAY = 0xA7
    MEMORYMODE = 0x20
    NORMALDISPLAY = 0xA6
    PAGEADDR = 0x22
    SEGREMAP = 0xA0
    SETCOMPINS = 0xDA
    SETCONTRAST = 0x81
    SETDISPLAYCLOCKDIV = 0xD5
    SETDISPLAYOFFSET = 0xD3
    SETHIGHCOLUMN = 0x10
    SETLOWCOLUMN = 0x00
    SETMULTIPLEX = 0xA8
    SETPRECHARGE = 0xD9
    SETSEGMENTREMAP = 0xA1
    SETSTARTLINE = 0x40
    SETVCOMDETECT = 0xDB
    SWITCHCAPVCC = 0x2
