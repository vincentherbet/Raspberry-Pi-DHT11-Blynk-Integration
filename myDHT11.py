import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
import adafruit_dht
import time
import board  

dht_device = adafruit_dht.DHT11(board.D18, use_pulseio=True)

BLYNK_AUTH_TOKEN = 'XNTGlkG_11KgKb8agu4oF-oGZCTh3cnR'

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
timer = BlynkTimer()

@blynk.on("connected")
def blynk_connected():
    print("Connected to Blynk Server!")
    time.sleep(2)  

def myData():
    try:
        
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9/5) + 32  
        humidity = dht_device.humidity
        
        print(f"Temp: {temperature_f:.1f} F / {temperature_c:.1f} C  Humidity: {humidity}%")

        blynk.virtual_write(0, temperature_c)
        blynk.virtual_write(1, humidity)
        print("Values sent to Blynk Server!")

    except RuntimeError as e:
        print(f"Sensor read error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

timer.set_interval(2, myData)

while True:
    blynk.run()
    timer.run()
