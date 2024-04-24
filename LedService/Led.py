import time
import subprocess
from rpi_ws281x import *

def color(r, g, b):
    return (r << 16) + (g << 8) + b

class StripLed:
    def __init__(self):
        self.playOnce=False
        self.ledCount = 30
        self.ledPin = 18
        self.ledFrequency = 800000
        self.ledBrightness = 10
        self.ledInvert = False
        self.ledChannel = 0
        self.ledDma = 10
        self.strip = Adafruit_NeoPixel(self.ledCount, self.ledPin, self.ledFrequency, self.ledDma, self.ledInvert, self.ledBrightness, self.ledChannel)
        self.strip.begin()

    def Startup(self):
        started = False
        self.SetColor(color(0, 0, 0))

        self.LoopBounce(color(0, 255, 0), color(255, 0, 0), color(0, 0, 0), color(0, 0, 0), 50)
        self.LoopBounce(color(0, 255, 0), color(255, 0, 0), color(0, 0, 0), color(0, 0, 0), 50)

        while not started:
            with open('/etc/LedService/started.txt', 'r') as f:
                started = f.read().strip() == 'True'
            self.SetColor(color(240, 120,15))
            self.Pulse()
        if started:
            self.LoopBounce(color(75, 255, 75), color(15, 255, 15), color(0, 0, 0), color(0, 0, 0), 50)
        self.ColorWipe(color(0, 0, 255))
        self.Loop()

    def SetColor(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def ColorWipe(self, color, wait_ms=50):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            self.Sleep1(wait_ms)

    def Pulse(self, wait_ms=8):
        for i in range(10, 85, 1):
            self.ledBrightness = i
            self.strip.setBrightness(self.ledBrightness)
            self.strip.show()
            self.Sleep1(wait_ms)
        for i in range(85, 10, -1):
            self.ledBrightness = i
            self.strip.setBrightness(self.ledBrightness)
            self.strip.show()
            self.Sleep1(wait_ms)

    def LoopBounce(self, color_1, color_2, color_back_1, color_back_2, wait_ms):
        for i in range(15, 31):
            self.strip.setPixelColor(i, color_2)
            self.strip.setPixelColor(29 - i, color_2)
            self.strip.show()
            self.Sleep1(35)
        for i in range(29, 14, -1):
            self.strip.setPixelColor(i, color_back_2)
            self.strip.setPixelColor(29 - i, color_back_1)
            self.strip.show()
            self.Sleep1(35)

    def Sleep1(self, wait_ms):
        try:
            time.sleep(wait_ms / 1000.0)
        except Exception as e:
            print("Sleep end with error:", e)

    def ping_google(self):
        try:
        # Exécuter la commande ping
            subprocess.run(["/usr/bin/ping", "-c", "1", "google.com"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
    def HandleWifiConnection(self, isConnected):
        if isConnected and not self.playOnce:
            for _ in range(5):
                self.Caterpillar(Color(0, 0, 255), Color(10, 255, 10))
            self.playOnce = True
        elif isConnected==False:
            self.playOnce=False
            self.Caterpillar(Color(0, 0, 255), Color(255, 0, 0))

    def Caterpillar(self, forwardColor, backwardColor):
        num_pixels = self.strip.numPixels()
        for i in range(num_pixels * 2):
            if i < num_pixels:
                self.strip.setPixelColor(i, forwardColor)
            else:
                self.strip.setPixelColor(num_pixels * 2 - i - 1, backwardColor)
            self.strip.show()
            self.Sleep1(23)

    def Loop(self):
        isConnected=self.ping_google()
        while True:
            self.HandleWifiConnection(isConnected)
            if isConnected:
                self.ColorWipe(Color(0,0,255))
                self.Pulse(15)
            isConnected=self.ping_google()
