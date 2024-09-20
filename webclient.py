import socket
import sys

# usage:
#   python webclient.py domain_name port:80
n = len(sys.argv)
if (n < 2) or (n > 3):
    print("usage: webclient.py domain_name port:80")
    sys.exit(1)
# print(sys.argv[0]) .\webclient.py

print("webclient start...")

char_encode = "UTF-8"
domain_name = sys.argv[1]
port = int(sys.argv[2]) if n == 3 else 80

# 1. make a new socket
s = socket.socket()

# 2. connect the socket to a destination
s.connect((domain_name, port))

# 3. build and send http request
simple_http_req = f"GET / HTTP/1.1" \
                  f"\r\n" \
                  f"Host: {domain_name}:{port}" \
                  f"\r\n" \
                  f"Connection: close" \
                  f"\r\n" \
                  f"\r\n"

req_bytes = simple_http_req.encode(char_encode)
s.sendall(req_bytes)

res_bytes = b""
# 4. receive the response
while True:
    b = s.recv(4096)
    if len(b) == 0:
        break
    res_bytes += b

res = res_bytes.decode(char_encode)
print(res)

# 5. close the socket
s.close()
