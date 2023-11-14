import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

baud_rate = 19200
port_name = '/dev/tty.usbmodem21201'

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



fig, ax = plt.subplots()
line_1, = ax.plot(time_1, LDR_Reading_1,color = 'red')
line_2, = ax.plot(time_2, LDR_Reading_2,color = 'blue')

def update(frame):
    global count
    time_1.append(count)
    time_2.append(count)

    data_1 = float(ser.readline().decode('utf-8').strip())
    data_2 = float(ser.readline().decode('utf-8').strip()) * 10
    
    LDR_Reading_1.append(data_1)
    LDR_Reading_2.append(data_2)

    count += 1
    line_1.set_data(time_1, LDR_Reading_1)
    line_2.set_data(time_2, LDR_Reading_2)
    ax.relim()
    ax.autoscale_view()

ani = FuncAnimation(fig, update, frames=range(1000), interval=1, repeat=False)

plt.show()
ser.close()