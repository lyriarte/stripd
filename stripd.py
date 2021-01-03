#!/usr/bin/python3

from rpi_ws281x import *
from fastapi import FastAPI

    
# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# LED strip initialization 
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


# FastAPI app instance
app = FastAPI()

# stripd API
@app.get("/STRIPLED/{index}/RGB/{color}")
def read_stripled_rgb(index: int, color: str):
	strip.setPixelColor(index, Color(int(color,16) >> 16, (int(color,16) & 0xFF00) >> 8, int(color,16) & 0xFF))
	strip.show()
	return {"led": index, "rgb": color}

@app.get("/GRADIENT/{src}/{srcrgb}/{dst}/{dstrgb}")
def read_gradient(src: int, srcrgb: str, dst: int, dstrgb: str):
	srcr = int(srcrgb,16) >> 16
	srcg = (int(srcrgb,16) & 0xFF00) >> 8
	srcb = int(srcrgb,16) & 0xFF
	dstr = int(dstrgb,16) >> 16
	dstg = (int(dstrgb,16) & 0xFF00) >> 8
	dstb = int(dstrgb,16) & 0xFF
	dr = dstr - srcr
	dg = dstg - srcg
	db = dstb - srcb
	for index in range(src, dst):
		delta = float(dst-index)/(dst-src)
		strip.setPixelColor(index, Color(min(255,max(0,dstr-int(dr*delta))), min(255,max(0,dstg-int(dg*delta))), min(255,max(0,dstb-int(db*delta)))))
	strip.show()
	return {"src": src, "dst": dst, "srcrgb": srcrgb, "dstrgb": dstrgb}

