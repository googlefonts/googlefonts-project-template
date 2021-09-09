from drawbot_skia.drawbot import *
from fontTools.ttLib import TTFont
from fontTools.misc.fixedTools import floatToFixedToStr
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output", metavar="PNG", help="where to write the PNG file")
args = parser.parse_args()

# Constants
WIDTH, HEIGHT, MARGIN, FRAMES = 2048, 2048, 128, 1
FONT_PATH = "fonts/ttf/Rubik-Regular.ttf"
AUXILIARY_FONT = "Helvetica"
AUXILIARY_FONT_SIZE = 48
BIG_TEXT = "Aa"

ttFont = TTFont(FONT_PATH)

# Constants we will work out dynamically
MY_URL = subprocess.check_output("git remote get-url origin", shell=True).decode()
MY_HASH = subprocess.check_output("git rev-parse --short HEAD", shell=True).decode()
MY_FONT_NAME = ttFont["name"].getDebugName(4)
FONT_VERSION = "v%s" % floatToFixedToStr(ttFont["head"].fontRevision, 16)

# Draws a grid
def grid():
    stroke(1, 0.2)
    strokeWidth(2)
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


# Remap input range to VF axis range
# (E.G. sinewave(-1,1) to wght(100,900))
def remap(value, inputMin, inputMax, outputMin, outputMax):
    inputSpan = inputMax - inputMin  # FIND INPUT RANGE SPAN
    outputSpan = outputMax - outputMin  # FIND OUTPUT RANGE SPAN
    valueScaled = float(value - inputMin) / float(inputSpan)
    return outputMin + (valueScaled * outputSpan)


# Draw page
newPage(WIDTH, HEIGHT)
fill(0)
rect(-2, -2, WIDTH + 2, HEIGHT + 2)
# grid() # uncomment to view a grid over the background

# Main text
fill(1)
stroke(None)
font(FONT_PATH)
fontSize(MARGIN * 8)
# Adjust this line to center main text manually.
# TODO: This should be done automatically when drawbot-skia
# has support for textBox() and FormattedString
text(BIG_TEXT, ((WIDTH / 2) - MARGIN * 4.75, (HEIGHT / 2) - MARGIN * 2.5))

# Divider lines
stroke(1)
strokeWidth(4)
lineCap("round")
line((MARGIN, HEIGHT - MARGIN), (WIDTH - MARGIN, HEIGHT - MARGIN))
line((MARGIN, MARGIN + (MARGIN / 2)), (WIDTH - MARGIN, MARGIN + (MARGIN / 2)))
stroke(None)

# Auxiliary text
font(AUXILIARY_FONT)
fontSize(AUXILIARY_FONT_SIZE)
POS_TOP_LEFT = (MARGIN, HEIGHT - MARGIN * 1.5)
POS_TOP_RIGHT = (WIDTH - MARGIN, HEIGHT - MARGIN * 1.5)
POS_BOTTOM_LEFT = (MARGIN, MARGIN)
POS_BOTTOM_RIGHT = (WIDTH - MARGIN * 0.9, MARGIN)
URL_AND_HASH = MY_URL + "at commit " + MY_HASH
URL_AND_HASH = URL_AND_HASH.replace("\n", " ")

text(MY_FONT_NAME, POS_TOP_LEFT, align="left")
text(FONT_VERSION, POS_TOP_RIGHT, align="right")
text(URL_AND_HASH, POS_BOTTOM_LEFT, align="left")
text("OFL v1.1", POS_BOTTOM_RIGHT, align="right")

# Save output
saveImage(args.output)
print("DrawBot: Done")
