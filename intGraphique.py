import tkinter as tk
import serial

# Connexion au port série du Raspberry Pi Pico
# Remplacez "/dev/ttyUSB0" par le port série correspondant à votre Raspberry Pi Pico
ser = serial.Serial('COM4')

def change_alert():
    new_alert = entry.get()
    ser = serial.Serial('COM4')
    ser.write(new_alert.encode())
    ser.close()

# Création de l'interface graphique
root = tk.Tk()

# Création d'un champ de saisie pour entrer la nouvelle valeur d'alerte
entry = tk.Entry(root)
entry.pack()

# Création d'un bouton pour envoyer la nouvelle valeur d'alerte
button = tk.Button(root, text='Change Alert Value', command=change_alert)
button.pack()

root.mainloop()
