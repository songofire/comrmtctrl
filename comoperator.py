from machine import Pin
import time,ubinascii

class ComOperator:
    __slots__ = ('pin5', 'pin18', 'pin19','pin25','pin26','udp_socket','v_flow_flag')
    
    def __init__(self,pin5,pin18,pin19,pin25,pin26,udp_socket,v_flow_flag):
        self.pin5 = pin5
        self.pin18 = pin18
        self.pin19 = pin19
        self.pin25 = pin25
        self.pin26 = pin26
        self.udp_socket = udp_socket
        self.v_flow_flag = v_flow_flag
    def v_check(self):
        print("pin25的电平:{},pin26的电平:{}".format(self.pin25.value(),self.pin26.value()))
        print("pin18的电平:{},pin19的电平:{}".format(self.pin18.value(),self.pin19.value()))
        print("pin25的电平:{},pin26的电平:{}".format(self.pin25.value(),self.pin26.value()))
        print("pin5的电平:{}".format(self.pin5.value()))
        print("flag的值为{}".format(self.v_flow_flag))
    
    def pull_down(self):
        self.pin5.value(1)
        time.sleep_ms(200)
        self.pin5.value(0)
    
    def long_pull_down(self):
        self.pin5.value(1)
        time.sleep_ms(2000)
        self.pin5.value(0)
    
    def com_state(self,is_print):
        result_str = 'off'
        count = 0
        for i in range(1,5,1):
            if(self.pin18.value() == 1):
                result_str = 'on'
                count = i
                break
            time.sleep_ms(20)
        if is_print:
            print('查询电脑状态为{},{}'.format(result_str,count))
        return result_str
    
    def power_on(self):
        state = self.com_state(True)
        if state == 'on':
            print('电脑已经为开机状态')
        else:
            self.pull_down()
            state = self.com_state(True)
        return state        
    def power_off(self):
        state = self.com_state(True)
        if state == 'off':
             print('电脑已经为关机状态')
        else:
            self.long_pull_down()
            state = self.com_state(True)
        return state  