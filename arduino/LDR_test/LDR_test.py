import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

baud_rate = 19200
port_name = '/dev/tty.usbmodem1234567890992'

ser = serial.Serial(port_name, baud_rate, timeout=1)

count = 0
LDR_Reading = []
time = []

for i in range(1,1001):
    time.append(i)

# Check if the port is open
if ser.is_open:
    print(f"Serial port {port_name} is open.")
else:
    print(f"Failed to open serial port {port_name}.")
    exit()

LDR_Reading = []
time = []
count = 0

fig, ax = plt.subplots()
line, = ax.plot(time, LDR_Reading)

def update(frame):
    global count
    time.append(count)
    LDR_Reading.append(float(ser.readline().decode('utf-8').strip()))
    count += 1
    line.set_data(time, LDR_Reading)
    ax.relim()
    ax.autoscale_view()

ani = FuncAnimation(fig, update, frames=range(1000), interval=1, repeat=False)

plt.show()
ser.close()
