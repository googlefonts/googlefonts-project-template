# RENDER THIS DOCUMENT WITH DRAWBOT: http://www.drawbot.com
# $ python3 image1.py
# COMPRESSED WITH: https://github.com/kornelski/pngquant
# $ brew install pngquant
# $ pngquant image.png
from drawbot_skia.drawbot import *

# CONSTANTS
WIDTH, HEIGHT, MARGIN, FRAMES = 2048, 2048, 128, 1

# DRAWS A GRID
def grid():
    stroke(1, 0.2)
    strokeWidth(1)
    STEP_X, STEP_Y = 0, 0
    INCREMENT_X, INCREMENT_Y = MARGIN / 2, MARGIN / 2
    rect(MARGIN, MARGIN, WIDTH - (MARGIN * 2), HEIGHT - (MARGIN * 2))
    for x in range(29):
        polygon((MARGIN + STEP_X, MARGIN), (MARGIN + STEP_X, HEIGHT - MARGIN))
        STEP_X += INCREMENT_X
    for y in range(29):
        polygon((MARGIN, MARGIN + STEP_Y), (WIDTH - MARGIN, MARGIN + STEP_Y))
        STEP_Y += INCREMENT_Y
    polygon((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    polygon((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


# REMAP INPUT RANGE TO VF AXIS RANGE
# (E.G. SINE WAVE(-1,1) to WGHT(100,900))
def remap(value, inputMin, inputMax, outputMin, outputMax):
    inputSpan = inputMax - inputMin  # FIND INPUT RANGE SPAN
    outputSpan = outputMax - outputMin  # FIND OUTPUT RANGE SPAN
    valueScaled = float(value - inputMin) / float(inputSpan)
    return outputMin + (valueScaled * outputSpan)


# DRAW PAGE
newPage(WIDTH, HEIGHT)
font("../fonts/ttf/MyFont-Regular.ttf")
fill(0)
rect(-2, -2, WIDTH + 2, HEIGHT + 2)
# grid() # Toggle for grid view


# MAIN TEXT
fill(1)
stroke(None)
fontSize(MARGIN * 8)
text("Aa", (MARGIN * 3.5, MARGIN * 5))


# MARGIN LINES
stroke(1)
strokeWidth(2)
line((MARGIN, HEIGHT - MARGIN), (WIDTH - MARGIN, HEIGHT - MARGIN))
line((MARGIN, MARGIN), (WIDTH - MARGIN, MARGIN))
stroke(None)


# AUXILIARY TEXT
font("Helvetica")
fontSize(48)
POS1l = (MARGIN, HEIGHT - MARGIN * 1.5)
POS1r = (WIDTH - MARGIN * 2, HEIGHT - MARGIN * 1.5)
text("My Font Regular", POS1l, align="left")
text("v1.000", POS1r, align="right")

POS2l = (MARGIN, MARGIN * 1.2)
POS2r = (WIDTH - MARGIN * 2, MARGIN * 1.2)
text("https://github.com/googlefonts/Unified-Font-Repository", POS2l, align="left")
text("OFL v1.1", POS2r, align="right")


# SAVE IMAGE
saveImage("image1.png")
print("DrawBot: Done")
