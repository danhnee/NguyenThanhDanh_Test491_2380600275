import socket

def port_scanner(host, port):
    # Socket object create lote tal
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Timeout htar dar ka port pait nay yin a kyar gyi ma saunt ag par
    s.settimeout(1)
    
    # Connection san kyi tal
    try:
        connection = s.connect_ex((host, port))
        if connection == 0:
            print(f"Port {port}: Open")
        s.close()
    except:
        pass

# Target IP nae port range ko thut mhat mal
target = "127.0.0.1" # Localhost mhar san kyi ya ag

print(f"Scanning {target}...")
for port in range(1, 101): # Port 1 ka nay 100 thi scan mal
    port_scanner(target, port)

print("Scan Finished.")