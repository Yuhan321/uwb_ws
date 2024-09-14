import re
import serial

def parse_data(data):
    # 改进的正则表达式来匹配数据
    match = re.match(r'mc (\w{2}) (\w{8}) (\w{8}) (\w{8}) (\w{8}) (\w{4}) (\w{2}) (\w{8}) t(\d):(\d+)', data)
    
    if match:
        # 解析匹配到的各个字段
        user = int(match.group(1), 16)
        range_vals = [int(match.group(i), 16) for i in range(2, 6)]
        lnum = int(match.group(6), 16)
        seq = int(match.group(7), 16)
        rangetime = int(match.group(8), 16)
        t_index = int(match.group(9))
        t_value = int(match.group(10))

        # 打印解析结果
        print(f"user=0x{user:02x}")
        print(f"range[0]={range_vals[0]}(mm)")
        print(f"range[1]={range_vals[1]}(mm)")
        print(f"range[2]={range_vals[2]}(mm)")
        print(f"range[3]={range_vals[3]}(mm)")
        # print(f"lnum=0x{lnum:04x}")
        # print(f"seq=0x{seq:02x}")
        # print(f"rangetime=0x{rangetime:08x}")
        # print(f"t_index={t_index}, t_value={t_value}")
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

