from pymodbus.client import ModbusTcpClient
import time

# مشخصات سرور Modbus TCP
MODBUS_SERVER_IP = '192.168.1.104'  # آدرس آی‌پی سرور
MODBUS_SERVER_PORT = 502           # پورت Modbus TCP (پیش‌فرض 502)

# آدرس‌های Modbus به صورت صفرپایه برای ورودی‌های دیجیتال (Discrete Inputs)
SENSOR_ADDRESSES = {
    'sensor_1': 0,    # معادل آدرس Modbus 10001
    'sensor_2': 1,    # معادل آدرس Modbus 10002
}

# تابعی برای خواندن داده‌ها از هر سنسور دیجیتال
def read_sensor(client, address):
    try:
        result = client.read_discrete_inputs(address, 1)  # خواندن یک ورودی دیجیتال از آدرس مورد نظر
        if not result.isError():
            return result.bits[0]  # داده‌های دیجیتال به صورت بیت برمی‌گردند
        else:
            print(f"Error reading address {address}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# اتصال به سرور Modbus
client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)

if client.connect():
    print("Connected to Modbus server")

    try:
        # حلقه اصلی برای خواندن و نمایش داده‌های سنسورهای دیجیتال
        while True:
            sensor_data = {}

            for sensor, address in SENSOR_ADDRESSES.items():
                value = read_sensor(client, address)
                if value is not None:
                    sensor_data[sensor] = value
                    print(f"{sensor}: {'ON' if value else 'OFF'}")
            
            print("-----------")

            # وقفه برای تکرار خواندن داده‌ها (به عنوان مثال هر 1 ثانیه)
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Program stopped by user.")
    
    finally:
        client.close()
        print("Disconnected from Modbus server")
else:
    print("Failed to connect to Modbus server")
