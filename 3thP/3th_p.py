import time
import I2C_LCD_drvier
mylcd = I2C_LCD_drvier.lcd()
mylcd.lcd_display_string("Booting Mode",1)
time.sleep(5)
mylcd.lcd_clear()
import requests
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import baco
import tts
import sys
reader = SimpleMFRC522()
rfid = ""
b_url = "http://192.168.0.80:8021/Leemart/bacode"
r_url = "http://192.168.0.80:8021/Leemart/rfid"
mode = False
GPIO.setwarnings(False)
mylcd.lcd_display_string("WaitingMode",1)
minute=0
while 1:
    if(not mode):
        try:
            id,text = reader.read()            
        finally:
            GPIO.cleanup()
        rfid = str(id)
        print(rfid)
        req = requests.post(r_url,data={"rfid":rfid})
        result =req.text
        if(result == 'able'):
            mylcd.lcd_clear()
            mylcd.lcd_display_string("IDDetect Exit",1)
            time.sleep(3)
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Shopping Mode",1)
            time.sleep(2)
            mylcd.lcd_clear()
            mode = True
    else:
        mylcd.lcd_display_string(rfid,1)
        b_code,minute = baco.bacode()
        req = requests.post(b_url,data={"b_num":b_code,"r_num":rfid,"time":minute})
        result = req.text
        print(result)
        if result == 'none':
            mylcd.lcd_display_string("NULL_Object",2)
            time.sleep(3)
            mylcd.lcd_clear()
        elif result.split(",")[0].split(" ")[0] == 'Exit':
                mylcd.lcd_clear()
                break
        else :
            result = result.split(",")
            event = result[0].split(" ")
            if(len(result)>1): ##
                name = event[0]
                eve = event[2]
                event[0] = baco.trans(name)
                info = event[0]+" "+event[1]
                mylcd.lcd_display_string(info,1)
                time.sleep(3)
                mylcd.lcd_clear()
                mylcd.lcd_display_string(result[1],2)
                time.sleep(3)
                mylcd.lcd_clear()
                if(eve != 'N/A'):
                    print('event')
                    tts.create_sound(name,eve)
                    tts.play_sound()
                mylcd.lcd_display_string(result[1],2)
mylcd.lcd_display_string("Exit Program",1)
time.sleep(5)
mylcd.lcd_clear()
sys.exit()