function doOLED (text: string) {
    OLED12864_I2C.clear()
    OLED12864_I2C.showString(
    0,
    0,
    text,
    1
    )
}
function doWater () {
    rekabit.runMotor(MotorChannel.M1, MotorDirection.Forward, 255)
    basic.pause(10000)
    rekabit.brakeMotor(MotorChannel.M1)
}
let index = 0
let plants: number[] = []
OLED12864_I2C.init(61)
OLED12864_I2C.on()
rekabit.setAllRgbPixelsColor(0x00ff00)
esp8266.init(SerialPin.P16, SerialPin.P15, BaudRate.BaudRate115200)
if (esp8266.isESP8266Initialized()) {
    doOLED("ESP8266 initialized success...")
} else {
    doOLED("ESP8266 initialized fail...")
}
esp8266.connectWiFi("summer_winds_guest", "")
if (esp8266.isWifiConnected()) {
    doOLED("WiFi success...")
} else {
    doOLED("WiFi fail...")
}
loops.everyInterval(3600000, function () {
    plants = [pins.analogReadPin(AnalogPin.P0), pins.analogReadPin(AnalogPin.P1)]
    for (let plant of plants) {
        if (plant > 600) {
            index = plants[plant]
            doOLED("Plant" + convertToText(index) + ": " + ("" + plant))
            esp8266.sendTelegramMessage("7089211278:AAENJMYzVjA-PtYKRFWfcOeFkI-JYnO2QJM", "-4104962273", "Plant" + convertToText(index) + ": " + ("" + plant))
            if (esp8266.isTelegramMessageSent()) {
                doOLED("Telegram success...")
            } else {
                doOLED("Telegram fail...")
            }
            esp8266.uploadThingspeak(
            "DUVSJOISR8YDA0R7",
            index,
            plant
            )
            if (esp8266.isThingspeakUploaded()) {
                doOLED("ThingSpeak success...")
            } else {
                doOLED("ThingSpeak fail...")
            }
            doWater()
        }
    }
})
