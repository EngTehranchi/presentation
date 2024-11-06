from pymodbus.client import ModbusTcpClient
import time


MODBUS_SERVER_IP = '192.168.1.104' 
MODBUS_SERVER_PORT = 502         


SENSOR_ADDRESSES = {
    'start_sensor': 0,    # آدرس سنسور اول (ابتدای نوار نقاله) معادل Modbus 10001
    'end_sensor': 1,      # آدرس سنسور دوم (انتهای نوار نقاله) معادل Modbus 10002
}

MOTOR_COIL_ADDRESS = 0 


def read_sensor(client, address):
    try:
        result = client.read_discrete_inputs(address, 1) 
        if not result.isError():
            return result.bits[0]  
        else:
            print(f"Error reading address {address}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def control_motor(client, status):
    try:
        result = client.write_coil(MOTOR_COIL_ADDRESS, status)  # ارسال فرمان به موتور
        if result.isError():
            print("Failed to send command to motor.")
        else:
            print("Motor ON" if status else "Motor OFF")
    except Exception as e:
        print(f"Error: {e}")




# اتصال به سرور Modbus
client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)

if client.connect():
    print("Connected to Modbus server")

    try:
        conveyor_running = False  


        while True:
            # خواندن وضعیت سنسورهای ابتدا و انتها
            start_sensor = read_sensor(client, SENSOR_ADDRESSES['start_sensor'])
            end_sensor = read_sensor(client, SENSOR_ADDRESSES['end_sensor'])

            if start_sensor and not conveyor_running:
                # اگر سنسور اول فعال شد و نوار نقاله خاموش است، موتور را روشن کن
                control_motor(client, True)
                conveyor_running = True

            elif end_sensor and conveyor_running:
                # اگر سنسور دوم فعال شد و نوار نقاله روشن است، موتور را خاموش کن
                control_motor(client, False)
                conveyor_running = False
            

            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Program stopped by user.")
    
    finally:
        client.close()
        print("Disconnected from Modbus server")
else:
    print("Failed to connect to Modbus server")
