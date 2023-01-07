# comrmtctrl 开机棒
simple device on remote controling computer  power and checking its state with esp chip and eletric relay
# 比某宝的优势
- mqtt通讯和socket通讯,接入HomeAssistant
- 装置无论什么状态断电/恢复电/插拔线/重启/等等都不影响主机状态
- 有开发能力可以自定义更多功能
- 简单低成本制作
# 接线
esp32 vcc -> 继电器电源正极  
esp32 gnd -> 继电器电源负极  
esp32 pin5 -> 继电器信号触发(高电平触发)  

继电器 NO -> esp32 gnd  
继电器 NC -> 不接  
继电器 COM -> 电脑 JFP1 6 引脚  
