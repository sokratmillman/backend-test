import socket
import threading
import json

FORMAT = "utf-8"

def handle_controller(conn, addr):
    print("RECONNECTED")
    conn.listen()
    try:
        conn1, addr1 = conn.accept()
        conn1.send("Hello".encode(FORMAT))
        while True:
            msg = json.loads(conn1.recv(1024).decode(FORMAT))
            print(json.dumps(msg))
            conn1.send("Received".encode(FORMAT))
    except KeyboardInterrupt:
        print("Aborting")
    except Exception as err:
        print("Some other error " + str(err))


def main():
    IP = "0.0.0.0"
    PORT = 32007
    address = (IP, PORT)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(address)
        print(f"Started on {address}")
    except:
        print("Error while trying")
        exit(0)
    server.listen()
    while (True):
        conn, addr = server.accept()
        port_free = False
        newport = PORT+1

        while not(port_free):
            try:
                new_address = (IP, newport)
                thread_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                thread_socket.bind(new_address)
                thread_socket.settimeout(5)
                thread = threading.Thread(target=handle_controller, args=(thread_socket, addr))
                thread.start()
                conn.send(f"{newport}".encode(FORMAT))
                conn.close()
                port_free = True
            except Exception as err:
                print("EXCEPTION occured", err)
                newport+=1

if __name__=="__main__":
    main()