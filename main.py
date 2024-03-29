def doOLED(text: str):
    OLED12864_I2C.clear()
    OLED12864_I2C.show_string(0, 0, text, 1)
def doWater():
    rekabit.run_motor(MotorChannel.M1, MotorDirection.FORWARD, 255)
    basic.pause(10000)
    rekabit.brake_motor(MotorChannel.M1)
index = 0
plants: List[number] = []
OLED12864_I2C.init(61)
OLED12864_I2C.on()
rekabit.set_all_rgb_pixels_color(0x00ff00)
esp8266.init(SerialPin.P16, SerialPin.P15, BaudRate.BAUD_RATE115200)
if esp8266.is_esp8266_initialized():
    doOLED("ESP8266 initialized success...")
else:
    doOLED("ESP8266 initialized fail...")
esp8266.connect_wi_fi("summer_winds_guest", "")
if esp8266.is_wifi_connected():
    doOLED("WiFi success...")
else:
    doOLED("WiFi fail...")

def on_every_interval():
    global plants, index
    plants = [pins.analog_read_pin(AnalogPin.P0),
        pins.analog_read_pin(AnalogPin.P1)]
    for plant in plants:
        if plant > 600:
            index = plants[plant]
            doOLED("Plant" + convert_to_text(index) + ": " + ("" + str(plant)))
            esp8266.send_telegram_message("7089211278:AAENJMYzVjA-PtYKRFWfcOeFkI-JYnO2QJM",
                "-4104962273",
                "Plant" + convert_to_text(index) + ": " + ("" + str(plant)))
            if esp8266.is_telegram_message_sent():
                doOLED("Telegram success...")
            else:
                doOLED("Telegram fail...")
            esp8266.upload_thingspeak("DUVSJOISR8YDA0R7", index, plant)
            if esp8266.is_thingspeak_uploaded():
                doOLED("ThingSpeak success...")
            else:
                doOLED("ThingSpeak fail...")
            doWater()
loops.every_interval(3600000, on_every_interval)
