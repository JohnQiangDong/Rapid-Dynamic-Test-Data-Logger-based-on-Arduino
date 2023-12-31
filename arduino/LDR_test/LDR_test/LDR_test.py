import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

baud_rate = 19200
port_name = '/dev/tty.usbmodem1234567890992'
#port_name = '/dev/tty.usbmodem21401'

ser = serial.Serial(port_name, baud_rate, timeout=1)

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
    LDR_Reading.append(float(ser.readline().decode('utf-8').strip())) # '\n' needs to be included in the sending data, to let python know the end of data
    count += 1
    line.set_data(time, LDR_Reading)
    ax.relim()
    ax.autoscale_view()

ani = FuncAnimation(fig, update, frames=range(1000), interval=1, repeat=False)
plt.show()

ser.close()

