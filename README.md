# UUV-from0to1

## 硬件
- 左右艉部推进器、中部垂直推进器、稳定舵
- 底层控制板用STM32，实现对推进器转速和舵角的控制，最终控制机器人姿态
- 上位机采用Jetson Nano，实现控制指令下发和环境图像数据采集、处理
- 机器人搭载ZED2双目相机，可以实现目标识别、检测和slam等功能

## 文件说明
### 0_Firmware_F407 V0.1(FreeRTOS)
- keil程序，解算DMP数据得到姿态角，并实现姿态PID控制
### 1_AUVControl_pcb
- 底层PCB文档，用立创EDA打开编辑，底层控制芯片采用STM32F407VET6  

![image](https://github.com/Yunga-Wu/UUV-from0to1/blob/main/img/PCB.jpg)

