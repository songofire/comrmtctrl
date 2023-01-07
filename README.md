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
esp32 GPIO 5 -> 继电器信号触发(高电平触发)  
esp32 gnd -> 主板 JFP1 PowerSwitch(8)  

esp32 GPIO 18 -> 主板 JFP1 PowerLed +  
esp32 GPIO 19 -> 主板 JFP1 PowerLed -  

继电器 NO -> esp32 gnd  
继电器 NC -> 不接  
继电器 COM -> 主板 JFP1 PowerSwitch(6)  

机箱按钮开关引脚 -> 主板 JFP1 PowerSwitch + 和 PowerSwitch -(接法和改造前一样,变成并联)  
机箱 HDD LED 引脚 -> 主板 JFP1 HDD LED + 和 HDD LED -(接法和改造前一样)
