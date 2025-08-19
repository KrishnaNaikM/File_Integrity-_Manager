import hashlib
from time import sleep
import winsound
import keyboard
import threading
import os

print("Hey! You are Currently Using File Integrity Monitoring Software")
print("This helps you maintain the integrity and security of your files.\n")

print(r" _   _            _   __        __            _ ")
print(r"| | | | __ _  ___| | _\ \      / /__  ___  __| |")
print(r"| |_| |/ _` |/ __| |/ /\ \ /\ / / _ \/ _ \/ _` |")
print(r"|  _  | (_| | (__|   <  \ V  V /  __/  __/ (_| |")  
print(r"|_| |_|\__,_|\___|_|\_\  \_/\_/ \___|\___|\__,_|")
print("\n")

filepath = input("Please Enter The File Path: ").strip()

def gethash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            while chunk := file.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def play_alert_sound():
    frequency = 2500  # Hertz
    duration = 1000   # Milliseconds
    winsound.Beep(frequency, duration)

print("[*] Calculating initial file hash...")
sleep(0.25)

BaseLine = gethash(filepath)

if BaseLine is None:
    print("[!] ERROR: File not found at the provided path.")
    exit()

print("[*] Monitoring started... Press 's' to stop monitoring.\n")

def monitor_file(filepath):
    global stop_monitoring
    while not stop_monitoring:
        current_hash = gethash(filepath)

        if current_hash is None:
            print("[!] ALERT: The file was deleted, renamed, or moved! \U0001F6A8")
            play_alert_sound()
            break  # Stop monitoring after alerting
        elif current_hash != BaseLine:
            print("[!] SECURITY ALERT: File has been changed or edited! \U0001F6A8")
            play_alert_sound()
            sleep(0.25)
        else:
            print("✅ Your file is safe.")
            sleep(2)

stop_monitoring = False

# Start the file monitoring in a separate thread
monitor_thread = threading.Thread(target=monitor_file, args=(filepath,))
monitor_thread.start()

# Stop the script if 's' key is pressed
keyboard.wait('s')
stop_monitoring = True
monitor_thread.join()

print("Monitoring stopped.")
