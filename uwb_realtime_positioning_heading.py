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

# 解析串口数据并更新 distanceArray 和航向角度 yaw
def parse_data(data):
    # 匹配数据并提取距离和航向角度
    pattern = re.compile(r'mi,(\d+\.\d+),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),T(\w+)')
    match = pattern.match(data)
    
    if match:
        # 提取距离数据并更新 distanceArray
        distances = [float(match.group(i)) if match.group(i) != "null" else -1 for i in range(2, 10)]
        for i in range(4):  # 更新前4个距离值
            distanceArray[i] = int(distances[i] * 1000) if distances[i] != -1 else -1  # 将距离转换为毫米
        
        # 提取航向角度 yaw
        yaw = float(match.group(21))
        
        # 打印解析结果
        print(f"Updated distances: A0={distanceArray[0]}(mm), A1={distanceArray[1]}(mm), A2={distanceArray[2]}(mm), A3={distanceArray[3]}(mm)")
        print(f"Yaw: {yaw:.3f}°")

        return yaw  # 返回航向角度

    else:
        print("Data format not recognized.")
        return None

# 实时从串口读取数据并更新距离和航向
def read_and_update_serial(port='/dev/ttyUSB0', baudrate=115200):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Reading data from {port}...")
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Raw data: {line}")
                yaw = parse_data(line)

                if yaw is not None:
                    # 调用定位函数
                    result = lib_so.GetLocation(ctypes.byref(location), anchorArray, distanceArray)

                    # 输出计算得到的位置和航向角度
                    print(f"Location: x={location.x:.3f}, y={location.y:.3f}, z={location.z:.3f}")
                    print(f"Yaw: {yaw:.3f}°")
                    print(f"Result: {result}")

if __name__ == "__main__":
    read_and_update_serial('/dev/ttyUSB0', 115200)  # 设置波特率为 115200
