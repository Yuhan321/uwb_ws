#①查看串口
sudo dmesg | grep tty
#②所有用户（包括文件所有者、文件所在组的用户，以及其他所有用户）都拥有读写权限
sudo chmod 666 /dev/ttyUSB0
或
sudo usermod -aG dialout $USER
#③安装 pySerial
pip install pyserial
#如果你希望 pyserial 模块在所有 Python 环境中都可用，可以全局安装 pyserial：
#sudo pip3 install pyserial
#④解析数据，查看数据--mc--T0到A0，A1，A2，A3的距离
python parse_mc_data.py
#④解析数据，查看数据--mi
#Raw data: mi,1778.565,10.90,10.66,3.22,3.27,null,null,null,null,0.450,-9.824,-0.010,0.003,-0.001,0.004,-11.700,41.700,5.250,-89.911,-1.704,-8.355,T0
#Time: 1778.565 s
#Distances: ['10.90 m', '10.66 m', '3.22 m', '3.27 m', 'null', 'null', 'null', 'null']
#Accelerations: [0.45, -9.824, -0.01] m/s^2
#Angular Velocities: [0.003, -0.001, 0.004] rad/s
#Magnetic Fields: [-11.7, 41.7, 5.25] uT
#Pitch: -89.911°
#Roll: -1.704°
#Yaw: -8.355°
#Tag ID: 0
python parse_mc_data.py
#如果数据正常，可以关掉④执行⑤
#⑤通过三边定位算法计算T0位置
python uwb_realtime_positioning.py
#⑤通过三边定位算法计算T0位置和航向
python uwb_realtime_positioning_heading.py
