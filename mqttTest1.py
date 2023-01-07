import time
import machine
import network
import ubinascii
from umqttsimple import MQTTClient, MQTTException
 
# ESP32连接无线网
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('xxx', 'xxx')  # WIFI名字和密码
        i = 1
        while not wlan.isconnected():
            print("正在链接中...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())
 
 
def sub_cb(topic, msg,client): # 回调函数，收到服务器消息后会调用这个函数
    print(topic,msg)
        
 
# 1. 联网
do_connect()
#2. 创建mqtt
c = MQTTClient(
        client_id = "com_rmt_ctrl",
        server= "xxx.xxx.xxx.xxx",
        port = 1883,
        user = "xxx",
        password = "xxx"
        )  # 建立一个MQTT客户端，这个IP是电脑的IP地址

c.set_callback(sub_cb)  # 设置回调函数
c.connect()  # 建立连接

topic_str = "/ha/room/com1/cmd".encode()

c.subscribe(topic_str) #指令频道
c.subscribe(b"/ha/room/com1/stat") #状态频道


while True:
    c.check_msg()
    time.sleep_ms(200)