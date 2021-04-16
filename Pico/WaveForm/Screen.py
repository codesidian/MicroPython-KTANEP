from machine import Pin, SoftSPI, PWM, ADC
from ST7735 import TFT, maker
from time import time, sleep
from math import sin,pi,cos
import random

spi = SoftSPI(baudrate=2400000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(1), miso=Pin(17))
oled = TFT(spi, 0, 3, 4)
oled.initb2()
oled.rgb(True)

oled.fill(TFT.BLACK)
sleep(0.25)
pixels = []

Sample_Rate=1000    # sample rate | "resolution" of the sampling
frequency=20        # the frequency of the signal, lower = slower
amplitude=60        # max/shift value

potentiometerR = ADC(Pin(26))
potentiometerL = ADC(Pin(27))

class Wave:
    def __init__(self, data, colour):
        self.data = data
        self.colour = colour


def get_sine(SAMPLE_RATE, FREQUENCY, TIME):
    "Calculate a sine wave"
    return sin(2*pi*FREQUENCY*TIME/SAMPLE_RATE);

def get_cosine(SAMPLE_RATE, FREQUENCY, TIME):
    "Calculate a cosine wave"
    return cos(2*pi*FREQUENCY*TIME/SAMPLE_RATE);

def shift(NUMBER, AMPLITUDE):
    "Shift the value according to the Amplitude"
    shift_val = (AMPLITUDE/2)+0.5
    return (shift_val*NUMBER)+shift_val;

def clean_round(NUMBER):
    "Round off and remove trailing decimals"
    return int(NUMBER);

def sine(SR, FR, AMP, TIME):
    "Calculate and return the final sine value"
    return clean_round(shift(get_sine(SR,FR,TIME),AMP));


def cosine(TIME):
    "Calculate and return the final cosine value"
    return clean_round(shift(get_cosine(Sample_Rate,frequency,TIME),amplitude));

def generateWaveData():
    rSampleRate = 1000
    rFrequency = random.randint(0,65)
    rAmplitude = random.randint(0,65) + 60
    return [[sine(rSampleRate, rFrequency, rAmplitude, i),i] for i in range(160)]

def drawWave(data, colour):
    for pixel in data:
        oled.pixel(pixel,colour)
        
def getRandomColour():
    col = random.randint(0,2)
    if col == 0:
        return TFT.BLUE
    if col == 1:
        return TFT.GREEN
    if col == 2:
        return TFT.RED

t_end = time() + 40

#DEFAULT PARAMS
Sample_Rate=1000    # sample rate | "resolution" of the sampling
frequency=20        # the frequency of the signal, lower = slower
amplitude=60        # max/shift value

NUM_OF_TARGET_WAVES = 3

targetWaves = []

for i in range(NUM_OF_TARGET_WAVES):
    targetWave = Wave(generateWaveData(), getRandomColour())
    targetWaves.append(targetWave)
    
while time() < t_end:
    #Sample_Rate = int(potentiometerR.read_u16())/10
    amplitude= 60 + (potentiometerR.read_u16()/1000)
    frequency=int(potentiometerL.read_u16())/1000
    for wave in targetWaves:
        drawWave(wave.data, wave.colour)
    for i in range(160):
        oled.pixel([sine(Sample_Rate, frequency, amplitude, i),i], TFT.YELLOW)
    sleep(0.5)
    oled.fill(TFT.BLACK)
      
    
#oled.fill(TFT.BLACK)


