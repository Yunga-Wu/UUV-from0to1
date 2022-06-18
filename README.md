# UUV-from0to1

## 硬件
- 执行机构：左右艉部推进器、中部垂直推进器、稳定舵
- 底层控制芯片用STM32F407VET6，实现对推进器转速和舵角的控制，最终控制机器人姿态
- [推进器 ROVMakerT200](https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-24333018520.56.fd497b12fuX3O7&id=651658155786)，额定电压24V，最大功率300W，重200g，推力2Kgf
- 上位机采用树莓派，实现控制指令下发和环境图像数据采集、处理
- 机器人搭载ZED2双目相机，可以实现目标识别、检测和slam等功能  

![image](https://github.com/Yunga-Wu/UUV-from0to1/blob/main/img/%E5%B0%8F%E5%9E%8BAUV%E8%A3%85%E9%85%8D%E5%9B%BE.jpg)

## 文件说明

### pcb
- 底层PCB文档，用立创EDA打开编辑
- 主芯片STM32F407VET6
- 系统晶振8M
- 12V锂电池电源，经降压稳压模块得到5V和3.3V，分别为Nano和stm32供电
- 推进器电机电压12V，舵机、GPS、无线和IMU电压5V
- 串口通信：GPU、无线、IMU、Nano（串口1）
- IIC通信：MPU6050
- 1颗红色供电指示灯：上电亮
- 3颗绿色电量指示灯：指示电量

![image](https://github.com/Yunga-Wu/UUV-from0to1/blob/main/img/pcb.jpg)

### stm32程序
- keil程序，用PS2下发航行控制指令，通过解算DMP数据得到当前姿态角，实现PID姿态控制
- 推进器需要运行相应的初始化程序

### raspi
- Raspberry pi的ROS功能包
- 实现功能：
   - 与地面站通信
   - 读取机器人传感器数据
   - PID参数可视化调节
   - 控制指令下发
   - 目标检测

## 调试日志
### 1.stm32
#### 程序线程
- 考虑稳定性和防止程序臃肿，没有用到FreeRTOS
- 用看门狗实现程序稳定运行，在中断中循环喂狗
#### 初始化程序
- 初始化：中断优先级分组、延时函数、串口、MPU6050、LED、定时器（PWM）、PS2、PID控制器结构体、电机
- 系统时钟频率8M
- 采样频率50Hz
- 中断优先级分组为2
#### PWM波和控制指令
- STM32的定时器只有1、2通道可以用作编码器模式，且此时定时器的其他通道只能用作普通IO口，不能复用
- 定时器TIM3的1、2、3、4通道分别复用为垂直推进器、左水平推进器、右水平推进器、舵机的PWM输出
- PWM自动重装载值20000-1，预分频系数84-1，PWM频率50Hz
- 推进器电机初始化程序：首先PWM占空比设置2000，延时1.5s；然后PWM占空比设置1500，延时1.5s；一共听到两声响动，初始化完成
- 当推进器电机PWM占空比为1750-1950时正转，占空比为1550~1750时反转，（PWM占空比不能给满）
- 由于推进器没有编码器，只能用IMU数据做PID控制的反馈输入
- 位置式PID
- 用PS2手柄下发航向角和深度指令，AUV做出姿态响应
#### 上传和接收数据
- 发送数据在while主循环的SendToUbuntu()函数中，接收数据在串口中断中
- 上传数据协议：协议头、设置航向角、设置纵倾角、当前航向角、当前纵倾角、电池电压、航向角PID参数、纵倾角PID参数、协议尾
- 接收数据：协议头、设置航向角、设置纵倾角、航向角PID参数、纵倾角PID参数

### 2.Raspberry pi
#### 环境准备操作
- 烧写系统步骤：
   1. SD卡选型： 树莓派3B要求大于16G，树莓派4B要求大于32G，Jetson nano要求大于32G
   2. SD卡格式化：SD Card Formatter
   3. 烧写：Win32Diskimager.exe 或者 balenaEtcher.exe
   4. 树莓派刷入新系统镜像，空间只有刷入镜像大小，需要配置系统空间扩充到整个SD卡：
      1. 打开新终端，输入： `sudo raspi-config`
      2. 选择`Advanced Options`选项
      3. 选择`Expand Fileststem`，回车，重启系统
      4. 打开新终端，输入： `df -h`，查看扩容是否成功
- 备份系统：
   1. 将插入SD的读卡器插入树莓派，并确认产生/dev/sda或/dev/sdc设备节点
   2. 运行系统备份脚本（脚本路径: /home/huike/backup.sh）：
      ```
      cd /home/huike/
      ./backup.sh
      ```
      - 不要采用远程登录的方式，由于拷贝时间过长，中端断开意味着进程结束
      - 确保用普通用户权限执行，sudo会产生系统拷贝出错
   3. 中端输出: `All done. You can un-plug the backup device`，说明备份成功!
   4. 备份结束后，会在SD卡产生树莓派的系统镜像，拷贝到windows后即可烧写系统进行刷机操作
- 树莓派系统ID：huike 密码： huike
- 固定IP： 192.168.12.1
- 局域网： Huanyu-111, 密码：12345678
- 配置局域网：`subl .bashrc`
   ```
   export ROS_MASTER_URI=http://192.168.12.1:11311
   export ROS_HOSTNAME=192.168.12.xx # turn this value to your PC's IP
   ```
- 如果没有键盘、鼠标和显示器，可以远程挂载树莓派：
   - 重启远程挂载： sudo /etc/init.d/nfs-kernel-server restart
   - 建立挂载： sudo mount nfs 192.168.12.1:/home/huanyu/robot_ws /mnt/
   - 取消挂载： sudo unmount /mnt
- 树莓派远程连接： ssh huike@192.168.12.1
- 设置网络
   1. 打开新终端，输入： `vim /etc/rc.local`
   2. 修改文件： `eth-enId Wifi_name Wifi_code &`
   3. 保存推出，重启系统，OK
#### 几个常用launch
- 底盘: `roslaunch huanyu_robot_start Huanyu_robot_start.launch`
- 手柄： `roslaunch huanyu_joy huanyu_ps2_control.launch`
#### PID参数可视化调节
- 所有电机共享一套PID参数
- 相关文件：
   - pic.cfg
   - Huanyu_robot.cpp
   - Huanyu_robot.h
   - Huanyu_robot_start.launch
- 打开可视化调节界面：`rosrun rqt_reconfigure rqt_reconfigure`
#### 读取机器人传感器数据和发布控制指令
- 文件：Huanyu_robot.cpp
- 里程计原理：对速度和角速度积分，得到位移和航向角
- 里程计代码：
   ```
   double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
   double delta_y = (vx * sin(th) - vy * cos(th)) * dt;
   double delta_th = vth * dt;
   x += delta_x;
   y += delta_y;
   th += delta_th;
   ```
- 好
#### 双目深度相机使用
- ROS功能包
   - 只获取彩色图像： huanyu_robot_start/launch/camera_image.launch
      ```roslaunch huanyu_robot_start camera_image.launch
   - 同时获取彩色和深度图像： astra_camera/ros_astra_launch/includes/astra.launch
      ```roslaunch ros_astra_launch astra.launch```
#### 目标检测
1. 启动彩色相机节点： `roslaunch huanyu_robot_start astra_rgb_ir_depth.launch`
2. Darknet节点： `roslaunch darknet_ros darknet_ros.launch
3. rviz中加载image消息，选择/darknet_ros/detection_image话题，可以看到检测的结果
#### 深度学习、神经网络相关功能
- 敬请期待。。。

   

## Reference
- 【1】[Huanyu Forum](http://huanyu-robot.uicp.hk/)
