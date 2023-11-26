import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

baud_rate = 19200
#port_name = '/dev/tty.usbmodem1234567890992'
port_name = '/dev/tty.usbmodem21101'

ser = serial.Serial(port_name, baud_rate, timeout=1)

count = 0
LDR_Reading_1 = []
LDR_Reading_2 = []
time_1 = []
time_2 = []
 
# Check if the port is open
if ser.is_open:
    print(f"Serial port {port_name} is open.")
else:
    print(f"Failed to open serial port {port_name}.")
    exit()

LDR_Reading_1.append(ser.readline().decode('utf-8').strip())
LDR_Reading_1.append(float(ser.readline().decode('utf-8').strip()))
LDR_Reading_1.append(float(ser.readline().decode('utf-8').strip()))
LDR_Reading_1.append(float(ser.readline().decode('utf-8').strip()))
LDR_Reading_1.append(float(ser.readline().decode('utf-8').strip()))
LDR_Reading_1.append(float(ser.readline().decode('utf-8').strip()))
for i in range(0,6):
    time_1.append(i)
print(LDR_Reading_1)
#plt.plot(LDR_Reading_1,time_1)
#plt.show()