import os.path
import socket
import sys

import Http
import StrUtil

# usage:
#   python webserver.py [port] ( default port: 28333 )


n = len(sys.argv)
if n < 1 or n > 2:
    print("usage: python webserver.py [port]")
    sys.exit(1)

print("webserver start...")

char_encode = "UTF-8"

# 1. make a new socket and set up it
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 2. bind to a port
port = int(sys.argv[1]) if n == 2 else 80
s.bind(("", port))

# 3. start listening
s.listen()

# 4. accept new connections
while True:
    new_conn = s.accept()  # 阻塞方法
    print("a new connection accepted...")

    new_socket = new_conn[0]

    # 5. receive the request from the client
    req_bytes = b""
    while True:
        b = new_socket.recv(4096)
        req_bytes += b
        if len(b) < 4096:
            break
        print(1)
        print(req_bytes)

    # initiate a HttpRequest object according to the HTTP Request Packet
    req = Http.HttpRequest(req_bytes)
    print(req)

    # 解析请求路径
    file = ""
    path = req.url
    if path == "/":
        file = "index.html"
    else:
        file = path.split("/", 1)[-1]

    fileName = os.path.split(file)[-1]
    ext = os.path.splitext(fileName)[-1]
    mime = StrUtil.getMIME(ext)

    # 6. send the response
    # 打开本地文件
    try:
        with open(file, "rb") as f:
            data = f.read()
            code = 200
            mime = StrUtil.getMIME(ext)
            f.close()
    except:
        with open("404.html", "rb") as f404:
            data = f404.read()
            code = 404
            mime = "text/html"
            f404.close()

    # initiate a HttpResponse object
    res = Http.HttpResponse()
    res.code = code
    res.msg = Http.codeDict[str(code)]
    res.setHeader("Content-Type", mime)
    res.setHeader("Content-Length", len(data))
    res.body = data
    print(res)

    # serialize the HttpResponse and send it
    res_bytes = res.encode()
    new_socket.sendall(res_bytes)

    # 7. close current socket for entering the next loop 貌似一次发送的内容太少时, 底层的缓冲区没满, 不会发送消息
    new_socket.close()  # 关闭socket会强制刷新底层的缓冲区, 即再发送一次消息



