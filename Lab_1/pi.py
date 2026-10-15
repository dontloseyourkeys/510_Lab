# Import time library for delays
import time
# Import board library to access GPIO pins
import board
# Import Adafruit DHT library to read from DHT11 sensor
import adafruit_dht
# Import socket library for network communication
import socket
# Initialize DHT11 sensor on pin D4 with use_pulseio disabled
dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)
# Create a new socket object
s = socket.socket()
# Connect to the server. Use your laptop's IP
s.connect(('172.20.10.4', 12345))
# Start an infinite loop to continuously read and send data
while True:
try:
# Read temperature from the sensor
temp = dht.temperature
# Read humidity from the sensor
hum = dht.humidity
# Print the values to the console in formatted style
print(f"Temp: {temp:.1f}°C Humidity: {hum:.1f}%")
# Convert temperature and humidity to a string
data = str(temp) + " " + str(hum)
# Send the string data to the server through the socket
s.send(data.encode())
# Wait for 1 second before next reading
time.sleep(1)
# Catch any errors that happen while reading the sensor
except Exception as e:
# Print an error message if sensor reading fails
print("Error reading DHT11:", e)
# Close the socket connection (will never reach here in infinite loop)
s.close()