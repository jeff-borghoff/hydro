def doWater(index: number):
    rekabit.set_servo_position(ServoChannel.S1, 90)
    rekabit.disable_servo(ServoChannel.S1)
    rekabit.run_motor(MotorChannel.M1, MotorDirection.FORWARD, 128)
    basic.pause(5000)
    rekabit.brake_motor(MotorChannel.M1)
plants: List[number] = []
OLED12864_I2C.init(61)
OLED12864_I2C.on()
rekabit.set_all_rgb_pixels_color(0x00ff00)
esp8266.init(SerialPin.P16, SerialPin.P15, BaudRate.BAUD_RATE115200)
if esp8266.is_esp8266_initialized():
    OLED12864_I2C.show_string(0, 0, "ESP8266 initialized success...", 1)
else:
    OLED12864_I2C.show_string(0, 0, "ESP8266 initialized fail...", 1)
esp8266.connect_wi_fi("summer_winds_guest", "")
if esp8266.is_wifi_connected():
    OLED12864_I2C.show_string(0, 0, "WiFi success...", 1)
else:
    OLED12864_I2C.show_string(0, 0, "WiFi fail...", 1)

def on_every_interval():
    global plants
    plants = [pins.analog_read_pin(AnalogPin.P0),
        pins.analog_read_pin(AnalogPin.P1)]
    for plant in plants:
        if plant > 600:
            index2 = 0
            OLED12864_I2C.clear()
            OLED12864_I2C.show_string(0,
                0,
                "Plant" + convert_to_text(index2) + ": " + ("" + str(plant)),
                1)
            esp8266.send_telegram_message("7089211278:AAENJMYzVjA-PtYKRFWfcOeFkI-JYnO2QJM",
                "-4104962273",
                "Plant" + convert_to_text(index2) + ": " + ("" + str(plant)))
            if esp8266.is_telegram_message_sent():
                OLED12864_I2C.show_string(0, 0, "Telegram success...", 1)
            else:
                OLED12864_I2C.show_string(0, 0, "Telegram fail...", 1)
            esp8266.upload_thingspeak("DUVSJOISR8YDA0R7", index2, plant)
            if esp8266.is_thingspeak_uploaded():
                OLED12864_I2C.show_string(0, 0, "ThingSpeak success...", 1)
            else:
                OLED12864_I2C.show_string(0, 0, "ThingSpeak fail...", 1)
loops.every_interval(3600000, on_every_interval)
