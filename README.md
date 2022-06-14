# UUV-from0to1

## 硬件
- 左右艉部推进器、中部垂直推进器、稳定舵
- 底层控制板用STM32，实现对推进器转速和舵角的控制，最终控制机器人姿态
- 上位机采用Jetson Nano，实现控制指令下发和环境图像数据采集、处理
- 机器人搭载ZED2双目相机，可以实现目标识别、检测和slam等功能  

![image](https://github.com/Yunga-Wu/UUV-from0to1/blob/main/img/%E5%B0%8F%E5%9E%8BAUV%E8%A3%85%E9%85%8D%E5%9B%BE.jpg)

## 文件说明
### 0_Firmware_F407 V0.1(FreeRTOS)
- keil程序，用PS2下发航行控制指令，通过解算DMP数据得到当前姿态角，实现PID姿态控制
- 推进器需要运行相应的初始化程序
### 1_AUVControl_pcb
- 底层PCB文档，用立创EDA打开编辑，底层控制芯片采用STM32F407VET6  

![image](https://github.com/Yunga-Wu/UUV-from0to1/blob/main/img/pcb.jpg)

### 2_JetsonNano+ROS
- ROS功能包文件
- 实现功能：

## 调试日志
### 1.STM32的定时器只有1、2通道可以用作编码器模式，且此时定时器的其他通道只能用作普通IO口，不能复用
### 2.定时器TIM3的1、2、3、4通道分别对应水平舵、垂直推进器、左水平推进器、右水平推进器的PWM输出
### 3.PWM自动重装载值20000-1，预分频系数84-1，PWM频率50Hz
### 4.推进器电机初始化程序：首先PWM占空比设置2000，延时1.5s；然后PWM占空比设置1500，延时1.5s；一共听到两声响动，初始化完成
### 5.由于推进器没有编码器，只能用IMU数据做PID控制的反馈输入

