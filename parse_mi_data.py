import re
import serial

def parse_data(data):
    # 使用正则表达式来匹配数据
    pattern = re.compile(r'mi,(\d+\.\d+),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+|null),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),T(\w+)')
    match = pattern.match(data)
    
    if match:
        # 提取数据
        time = float(match.group(1))
        distances = [float(match.group(i)) if match.group(i) != "null" else None for i in range(2, 10)]
        accelerations = [float(match.group(i)) for i in range(10, 13)]
        angular_velocities = [float(match.group(i)) for i in range(13, 16)]
        magnetic_fields = [float(match.group(i)) for i in range(16, 19)]
        pitch = float(match.group(19))
        roll = float(match.group(20))
        yaw = float(match.group(21))
        tag_id = match.group(22)

        # 打印解析结果
        print(f"Time: {time:.3f} s")
        print(f"Distances: {['{:.2f} m'.format(d) if d is not None else 'null' for d in distances]}")
        print(f"Accelerations: {accelerations} m/s^2")
        print(f"Angular Velocities: {angular_velocities} rad/s")
        print(f"Magnetic Fields: {magnetic_fields} uT")
        print(f"Pitch: {pitch:.3f}°")
        print(f"Roll: {roll:.3f}°")
        print(f"Yaw: {yaw:.3f}°")
        print(f"Tag ID: {tag_id}")
    else:
        print("Data format not recognized.")

def read_and_parse_serial(port='/dev/ttyUSB0', baudrate=115200):
    # 打开串口
    with serial.Serial(port, baudrate, timeout=1) as ser:
        print(f"Reading data from {port}...")
        while True:
            # 从串口读取一行数据
            line = ser.readline().decode('utf-8').strip()
            if line:  # 如果读取到数据
                print(f"Raw data: {line}")
                parse_data(line)

if __name__ == "__main__":
    read_and_parse_serial('/dev/ttyUSB0', 115200)  # 设置波特率为 115200
