import paramiko
from paramiko import SSHClient
# from scp import SCPClient
# import subprocess
import sys

# adafruit display imports

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#def progress(filename, size, sent):


# SCPCLient takes a paramiko transport and progress callback as its arguments.
# scp = SCPClient(ssh.get_transport(), progress = progress)
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

authfile = open("auth.txt", "r")
authlist = authfile.readlines()
authlist[0] = authlist[0].strip('\n')
authlist[1] = authlist[1].strip('\n')

ssh.connect(hostname='192.168.7.125',username=authlist[0],password=authlist[1])


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
# image = Image.open('conan2.png').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

# time.sleep(5)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.open('IMG_8590.PNG').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')
disp.image(image)
disp.display()
time.sleep(5)

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
    #cmd = "hostname -I | cut -d\' \' -f1"
    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    #IP = ssh_stdout.read() #subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    CPU = ssh_stdout.read() #subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %d%%\", $3,$2,$3*100/$2 }'"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    MemUsage = ssh_stdout.read() #subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    Disk = ssh_stdout.read() #subprocess.check_output(cmd, shell = True )
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("tac /home/steve/steam/exiles/ConanSandbox/Saved/Logs/ConanSandbox.log | grep -oPm1 'players=\K\d+'")
    playerCount = ssh_stdout.read()
    Time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    ditkaFile = open('/home/pi/ditkaBot/HurricaneDitkaBot/conan.txt','w')
    conanStats = 'Conan Exiles players currently online: ' + playerCount.decode('utf-8')
    ditkaFile.write(conanStats)
    # Write two lines of text.

    #draw.text((x, top),       "IP: " + IP.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top),       Time,  font=font, fill=255)
    draw.text((x, top+8),     "Player Count: " + playerCount.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+16),    CPU.decode('utf-8'), font=font, fill=255)
    draw.text((x, top+24),    MemUsage.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+32),    Disk.decode('utf-8'),  font=font, fill=255)

    
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
