import network,time,_thread,ubinascii,machine
from machine import Pin
from comoperator import ComOperator
from umqttsimple import MQTTClient, MQTTException


ON_CMD = "on"
OFF_CMD = "off"
STATE_CMD = "state"
V_CHECK_CMD = "vcheck"
CHANGE_FLAG_CMD = "change flag"
ID = "comrmtctrl"
PULL_DOWN_CMD = "pulldown"

#自定义
CMD_TOPIC = "/test1/cmd"
STATE_TOPIC = "/test1/state"


def do_connect(ssid,key):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to net work...')
        wlan.connect(ssid,key)
        while not wlan.isconnected():
            pass
    print('network config',wlan.ifconfig())

def create_udp_socket():
    import socket
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0",7788))
    return udp_socket
 
#监听按钮
def button_onclick(com_operator):
    time.sleep_ms(200)
    
    while(True):   
        if com_operator.pin26.value() == 1:
            time.sleep_ms(200)
            if(com_operator.pin26.value() == 1):
                while(com_operator.pin26.value() == 1):
                    time.sleep_ms(200)
                com_operator.pin5.value(0)
                print("pin5的电平:{},pin25的电平:{},pin26的电平:{}".format(com_operator.pin5.value(),com_operator.pin25.value(),com_operator.pin26.value()))
                time.sleep_ms(200)
                com_operator.pin5.value(1)

#监听信息
def msg_recv(com_operator):
     while(True):
        recv_data,sender_info = com_operator.udp_socket.recvfrom(1024)    
        #print("{}发送数据:{}".format(sender_info,recv_data))
        recv_data_str = recv_data.decode("utf-8")
        print("解码后的数据:{}".format(recv_data_str))
        if recv_data_str == ON_CMD:
            com_operator.power_on()
        elif recv_data_str == OFF_CMD:
            com_operator.power_off()
        elif recv_data_str == V_CHECK_CMD:
            com_operator.v_check()
        elif recv_data_str == CHANGE_FLAG_CMD:
            if com_operator.v_flow_flag == 1:
                com_operator.v_flow_flag = 0
            else:
                com_operator.v_flow_flag = 1
            print('flag 的值为{}'.format(com_operator.v_flow_flag))
        elif recv_data_str == STATE_CMD:
            com_operator.com_state(True)


def led_v_print(com_operator):
    while(True):
        if com_operator.v_flow_flag == 1:  
            print("pin18的电平:{},pin19的电平:{}".format(com_operator.pin18.value(),com_operator.pin19.value()))
            time.sleep_ms(200)
        else:
            pass

def create_mqtt_client(client_id, com_operator):
    #自定义 创建 mqtt 客户端 
    c = MQTTClient(
            client_id = client_id,
            server= "xxx.xxx.xxx.xxx",
            port = 1883,
            user = "xxxxxx",
            password = "xxxxxx",
            com_operator = com_operator
            )  

    c.set_callback(sub_cb)  # 设置回调函数
    c.connect()
    if client_id.endswith("cmd"):
        c.subscribe(CMD_TOPIC.encode()) #指令频道
    return c

def mqtt_recv(c):
    while(True):
        try:
            c.check_msg()
            time.sleep_ms(20)
        except Exception as e:
            print(e)

def sub_cb(topic, msg, c, com_operator): # 回调函数，收到服务器消息后会调用这个函数
    msg = msg.decode("utf-8")
    print("收到频道[{}]的信息[{}]".format(topic,msg))
    state = 'NONE'
    if msg == ON_CMD:
        state = com_operator.power_on()     
    elif msg == OFF_CMD:
        state = com_operator.power_off()
    elif msg == STATE_CMD:
        state = com_operator.com_state(True)
    elif msg == PULL_DOWN_CMD:
        com_operator.pull_down()
    print("发布频道[{}]状态[{}]".format(STATE_TOPIC,state))
    c.publish(STATE_TOPIC.encode(), state.encode())

def state_pub(c):
    while(True):
        try:
            state = c.com_operator.com_state(False)
            #print("发布频道[{}]状态[{}]".format(STATE_TOPIC,state))
            c.publish(STATE_TOPIC.encode(), state.encode())
            time.sleep(2)
        except Exception as e:
            print(e)
    
def main():
    
    #Pin5 接继电器信号引脚
    pin5 = Pin(5,Pin.OUT,value=0)
    #机箱按键接 Pin25 Pin26
    pin25 = Pin(25,Pin.IN,Pin.PULL_UP)
    pin26 = Pin(26,Pin.IN)
    #主板 JFP1 2引脚 Power led+ 接 Pin18
    #主板 JFP1 4引脚 Power led- 接 Pin19
    pin18 = Pin(18,Pin.IN,Pin.PULL_DOWN)
    pin19 = Pin(19,Pin.IN,Pin.PULL_DOWN)
    
    #自定义,连接 wifi
    do_connect('xxx','xxx')
    udp_socket = create_udp_socket()
    
    #创建主机执行者
    com_operator = ComOperator(pin5,pin18,pin19,pin25,pin26,udp_socket,0)
    
    #连接 mqtt
    c = create_mqtt_client("comrmtctrl1_cmd", com_operator)
    
    #1.检测实体按钮
    #_thread.start_new_thread(button_onclick,(com_operator,))
    
    #2.接收 socket信息
    _thread.start_new_thread(msg_recv,(com_operator,))
    
    #3.led 引脚电压打印
    #_thread.start_new_thread(led_v_print,(com_operator,))
    
    #4.mqtt
    _thread.start_new_thread(mqtt_recv,(c,))
    
    #5.定时发布状态
    c2 = create_mqtt_client("comrmtctrl1_state", com_operator)
    _thread.start_new_thread(state_pub,(c2,))
    
    print('initialization compeleted ...')

if __name__ == '__main__':
    main()


