import network # WiFi networking
import time # Timing and delays
import dht # DHT temperature/humidity sensor driver
from machine import Pin, PWM # GPIO pin and PWM control
import neopixel # WS2812 addressable LED driver
from umqtt.simple import MQTTClient # Lightweight MQTT client

# ===== Pin Definitions =====
DHT_PIN = 12 # Data pin for the DHT22 sensor
LED_PIN = 26 # Pin driving the plain LED
SERVO_PIN = 2 # PWM pin driving the servo
NEO_PIN = 4 # Data pin for the NeoPixel strip
NUM_LEDS = 16 # Number of LEDs on the NeoPixel strip

# ===== MQTT & WiFi Configuration =====
WIFI_SSID = "Wokwi-GUEST" # Wokwi's built in open network
WIFI_PASS = "" # No password for Wokwi-GUEST
MQTT_SERVER = "broker.hivemq.com" # Public MQTT broker
CLIENT_ID = "ujaisldaaasdfgh_laslksdja1" # Unique client ID for this device

# ===== Topic Configuration =====
# Change the group number here only, every topic below rebuilds automatically
group_number = "group_10"
BASE_TOPIC = f"cps/topic/{group_number}" # Common prefix for all topics

TOPIC_PUB = f"{BASE_TOPIC}/Tempdata" # Device publishes temp/humidity here
TOPIC_LIGHTS = f"{BASE_TOPIC}/lights" # Subscribe: LED on/off
TOPIC_SERVO = f"{BASE_TOPIC}/servo" # Subscribe: servo angle
TOPIC_NEOPIXEL = f"{BASE_TOPIC}/lights/neopixel" # Subscribe: NeoPixel color
# ================================

# ===== Initialize Hardware =====
led = Pin(LED_PIN, Pin.OUT) # Configure LED pin as output
led.value(0) # Start with LED off

# DHT22 Setup
dht_sensor = dht.DHT22(Pin(DHT_PIN)) # Create the sensor object

# NeoPixel WS2812 Setup
np = neopixel.NeoPixel(Pin(NEO_PIN), NUM_LEDS) # Create the LED strip object

# Servo Setup (50Hz PWM)
servo_pwm = PWM(Pin(SERVO_PIN), freq=50) # Servos expect a 50Hz signa

def set_servo_angle(angle):
    """
    Maps 0-180 degrees to pulse width (500us to 2400us)
    matching ESP32Servo attach(SERVO_PIN, 500, 2400)
    """
    min_us = 500 # Pulse width for 0 degrees
    max_us = 2400 # Pulse width for 180 degrees
    
    # Linearly scale the requested angle to a pulse width in microseconds
    us = min_us + (angle / 180.0) * (max_us - min_us)
    
    # Convert microseconds to a 16 bit duty value (20,000us period at 50Hz)
    duty = int((us / 20000.0) * 65535)
    servo_pwm.duty_u16(duty) # Apply the duty cycle
    
    # Set initial servo position to 0 degrees
    set_servo_angle(0)
    
def setup_wifi():
    # Connect the board to WiFi in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True) # Turn on the WiFi interface
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        # Wait in a loop until the connection is established
    
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
    
    print("\nWiFi connected")
    print("IP address: ", wlan.ifconfig()[0]) # Show the assigned IP
    
def mqtt_callback(topic, msg):
    # Runs every time a subscribed topic receives a message
    topic_str = topic.decode("utf-8") # Convert topic bytes to string
    data_str = msg.decode("utf-8") # Convert payload bytes to string
    
    # Debug print of the incoming message
    print(f"Message arrived in topic: {topic_str}")
    print(f"Message: {data_str}")
    print(f"Message size: {len(data_str)}")
    print("-----------------------")
    print(data_str)
    
    # Handle LED control messages
    if topic_str == TOPIC_LIGHTS:
        if data_str == "ON":
            print("LED")
            led.value(1) # Turn LED on
        else:
            led.value(0) # Turn LED off for anything other than "ON"
  
    # Handle servo angle messages
    elif topic_str == TOPIC_SERVO:
        try:
            degree = int(data_str) # Payload should be a whole number
            print(f"Moving servo to degree: {degree}")
            set_servo_angle(degree)
        except ValueError:
            print("Invalid degree received") # Payload was not a valid integer
  
    # Handle NeoPixel color messages
    elif topic_str == TOPIC_NEOPIXEL:
        try:
            # Parse CSV payload into RGB integers
            red, green, blue = map(int, data_str.split(","))
            print(f"Setting NeoPixel color to (R,G,B): {red},{green},{blue}")
            np.fill((red, green, blue)) # Apply color to all LEDs
            np.write() # Push the color data to the strip
        except ValueError:
            print("Invalid color payload. Expected format: R,G,B")

# Connect Network
setup_wifi()

# ===== Setup MQTT Client =====
client = MQTTClient(CLIENT_ID, MQTT_SERVER) # Create the client
client.set_callback(mqtt_callback) # Register the message handler

def reconnect():
    # Keep trying to connect and subscribe until it succeeds
    while True:
        try:
            print("Connecting to MQTT broker...")
            client.connect()
            # Subscribe to all three control topics
            client.subscribe(TOPIC_LIGHTS)
            client.subscribe(TOPIC_SERVO)
            client.subscribe(TOPIC_NEOPIXEL)
            print("MQTT connected")
            print("Topic Subscribed")
            break # Exit the retry loop once connected
        except Exception as e:
            print(f"failed, error: {e} try again in 5 seconds")
            time.sleep(5) # Wait before the next attempt


reconnect()


# ===== Main Loop timing =====
previous_millis = time.ticks_ms() # Timestamp of the last publish
interval = 1000 # 1000 ms non-blocking delay

while True:
    try:
        # Non-blocking check for incoming MQTT messages
        client.check_msg()
    except OSError:
        reconnect() # Reconnect if the connection dropped
        
    current_millis = time.ticks_ms()
    # Only publish once per interval without blocking the loop
    if time.ticks_diff(current_millis, previous_millis) >= interval:
        previous_millis = current_millis # Reset the timer
        
        try:
            dht_sensor.measure() # Trigger a new sensor reading
            temp = dht_sensor.temperature() # Read temperature in Celsius
            hum = dht_sensor.humidity() # Read humidity in percent
            
            print(f"Temperature: {temp:.1f}°C")
            print(f"Humidity: {hum:.1f}%")
            
            # Build a CSV payload "temp,hum," and publish it
            msg_str = f"{temp:.1f},{hum:.1f},"
            print(f"PUBLISH DATA: {msg_str}")
            client.publish(TOPIC_PUB, msg_str.encode("utf-8"))
        
        except Exception as e:
            print("Error reading temperature/humidity!") # Sensor read failed
    
    time.sleep_ms(10) # Short sleep yield to keep system stable