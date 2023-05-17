import tkinter as tk
import serial
import threading

ser = serial.Serial('COM4')

def change_alert():
    new_alert = entry.get()
    ser.write(bytes(str(new_alert) + '\r\n', 'utf-8'))
    ser.flush()

def read_distance():
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            distance, alert_value = map(float, line.split(','))
            distance_label.config(text='Distance: {:.1f} cm'.format(distance))
            if distance < alert_value:
                alert_label.config(text='!!!!!! ALERT !!!!!!!', fg='red')
            else:
                alert_label.config(text='')

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text='Change Alert Value', command=change_alert)
button.pack()

distance_label = tk.Label(root, text='')
distance_label.pack()

alert_label = tk.Label(root, text='', fg='red')
alert_label.pack()

threading.Thread(target=read_distance, daemon=True).start()

root.mainloop()

ser.close()
