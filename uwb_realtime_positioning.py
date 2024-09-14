import ctypes
import re
import serial

# 加载共享库
lib_so = ctypes.cdll.LoadLibrary('./trilateration.so')

# 定义UWBMsg结构体
class UWBMsg(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("z", ctypes.c_double)]

# 初始化定位和测距数组
location = UWBMsg()
anchorArray = (UWBMsg * 8)()
distanceArray = (ctypes.c_int * 8)(-1)

# 设置基站位置
# A0(0,0,2) A1(0,5.28,2) A2(11.09,5.28,2) A3(11.09,0,2)
anchorArray[0].x = 0
anchorArray[0].y = 0
anchorArray[0].z = 2

anchorArray[1].x = 0
anchorArray[1].y = 5.28
anchorArray[1].z = 2

anchorArray[2].x = 11.09
anchorArray[2].y = 5.28
anchorArray[2].z = 2

anchorArray[3].x = 11.09
anchorArray[3].y = 0
anchorArray[3].z = 2

# 解析串口数据并更新 distanceArray
def parse_data(data):
    # 匹配数据并更新distanceArray中的值
    match = re.match(r'mc (\w{2}) (\w{8}) (\w{8}) (\w{8}) (\w{8}) (\w{4}) (\w{2}) (\w{8}) t(\d):(\d+)', data)
    if match:
        # 提取距离值并转换为整数
        range_vals = [int(match.group(i), 16) for i in range(2, 6)]
        distanceArray[0] = range_vals[0]  # tag to A0 distance
        distanceArray[1] = range_vals[1]  # tag to A1 distance
        distanceArray[2] = range_vals[2]  # tag to A2 distance
        distanceArray[3] = range_vals[3]  # tag to A3 distance

        # 打印解析结果
        print(f"Updated distances: A0={distanceArray[0]}(mm), A1={distanceArray[1]}(mm), A2={distanceArray[2]}(mm), A3={distanceArray[3]}(mm)")

# 实时从串口读取数据并更新距离
def read_and_update_serial(port='/dev/ttyUSB0', baudrate=115200):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Reading data from {port}...")
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Raw data: {line}")
                parse_data(line)

                # 调用定位函数
                result = lib_so.GetLocation(ctypes.byref(location), anchorArray, distanceArray)

                # 输出计算得到的位置
                print(f"Location: x={location.x}, y={location.y}, z={location.z}")
                print(f"Result: {result}")

if __name__ == "__main__":
    read_and_update_serial('/dev/ttyUSB0', 115200)  # 设置波特率为 115200
