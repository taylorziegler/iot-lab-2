import socket
import threading
import picar_4wd as fc
import time
from gpiozero import CPUTemperature

HOST = "10.0.0.224" # IP address of your Raspberry PI
PORT = 65526         # Port to listen on (non-privileged ports are > 1023)
global moving

lock = threading.Lock()

def forward():
    global moving
    fc.forward(-1)
    with lock:
        moving = "forward"
    time.sleep(2)
    with lock:
        moving = "no"
    fc.stop()

def backward():
    global moving
    fc.forward(1)
    with lock:
        moving = "backward"
    time.sleep(2)
    with lock:
        moving = "no"
    fc.stop()

def left():
    global moving
    fc.turn_left(1)
    with lock:
        moving = "left"
    time.sleep(2)
    with lock:
        moving = "no"
    fc.stop()

def right():
    global moving
    fc.turn_right(1)
    with lock:
        moving = "right"
    time.sleep(2)
    with lock:
        moving = "no"
    fc.stop()

def get_dist():
    return fc.get_distance_at(0)


def get_cpu_temp():
    cpu = CPUTemperature()
    return cpu.temperature


def handle_commands(client, s):
    print("handle commands thread start...")
    try:
        while True:
            data = client.recv(1024)
            print(data)
            if (data != b"\r\n"):
                command = data.strip()
                if data == b"87\r\n":        # forward
                    forward()
                    print("moving forward")
                elif data == b"83\r\n":      # backward
                    backward()
                    print("moving backward")
                elif data == b"65\r\n":      # left
                    left()
                    print("moving left")
                elif data == b"68\r\n":      # right
                    right()
                    print("moving right")
                else:
                    print("handle", command)
    except Exception:
        print("movement error")
        print("Closing socket")
        client.close()
        s.close()   

def send_sensor_data(client, s):
    print("send sensor data thread start...")
    global moving
    try:
        while True:
            temp = get_cpu_temp()
            dist = get_dist()
            with lock:
                data = str(temp) + ',' + str(dist) + ',' + moving
            print(data)
            client.sendall((data).encode())
            time.sleep(1)
    except:
        print("Closing socket")
        client.close()
        s.close()   
        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    moving = "no"

    try:
        
        while 1:
            client, clientInfo = s.accept()
            print("client %s connected", clientInfo)
            command_thread = threading.Thread(target=handle_commands, args=(client, s))
            sensor_thread = threading.Thread(target=send_sensor_data, args=(client, s))

            command_thread.start()
            sensor_thread.start()

            command_thread.join()
            sensor_thread.join()
    except : 
        print("Closing socket")
        client.close()
        s.close()    
