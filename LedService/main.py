import Led
try:
    led = Led.StripLed().Startup()
except Exception as e:
    print(e)
