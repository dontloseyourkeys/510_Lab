import time
import board
import adafruit_dht

# must use use_pulseio=False
dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)
while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        print(f"Temp: {temp:.1f}°C Humidity: {hum:.1f}%")
    except Exception as e:
# Any error from the DHT read will be caught here
        print("Error reading DHT11:", e)
    time.sleep(2)