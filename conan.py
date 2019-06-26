import paramiko
from paramiko import SSHClient
from scp import SCPClient
import subprocess
import sys

# adafruit display imports

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

# SCPCLient takes a paramiko transport and progress callback as its arguments.
# scp = SCPClient(ssh.get_transport(), progress = progress)
ssh= SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('connecting...')
ssh.connect(hostname='192.168.7.125',username='steve',password='steve')
print('connected.') # SCPClient takes a paramiko transport as an argument
scp = SCPClient(ssh.get_transport(), progress = progress)
print('getting file')
scp.get('/home/steve/steam/exiles/ConanSandbox/Saved/Logs/ConanSandbox.log')
print('file retrieved?')
scp.close()
print('scp closed')

cmd = "tac ConanSandbox.log | grep -oPm1 'players=\K\d+'"
playerCount = subprocess.check_output(cmd, shell = True )
print('Players: ' + playerCount.decode('utf-8'))

# adafruit stats.py implementation

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.

    draw.text((x, top),       "IP: " + IP.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+8),     CPU.decode('utf-8'), font=font, fill=255)
    draw.text((x, top+16),    MemUsage.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+24),    Disk.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+32),    "Player Count: " + playerCount.decode('utf-8'),  font=font, fill=255)
    
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)