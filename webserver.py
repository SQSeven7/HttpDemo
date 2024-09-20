import os.path
import socket
import sys
import StrUtil

# usage:
#   python webserver.py [port] ( default port: 28333 )


n = len(sys.argv)
if n < 1 or n > 2:
    print("usage: python webserver.py [port]")
    sys.exit(1)

print("webserver start...")
# test
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
    new_conn = s.accept()  # todo 阻塞方法
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
    req = req_bytes.decode(char_encode)

    print(req)

    # todo 解析请求路径
    file = ""
    path = StrUtil.matchPath(req)
    if path == "/":
        file = "index.html"
    else:
        file = path.split("/", 1)[-1]

    fileName = os.path.split(file)[-1]
    ext = os.path.splitext(fileName)[-1]
    mime = StrUtil.getMIME(ext)

    # 6. send the response
    # todo 打开本地文件
    try:
        with open(file, "rb") as f:
            data = f.read()
            status = 200
            f.close()
    except:
        with open("404.html", "rb") as f404:
            data = f404.read()
            status = 404
            mime = "text/html"
            f404.close()



    simple_http_res = StrUtil.httpPacket(status, mime, len(data))

    res_bytes = simple_http_res.encode(char_encode)
    new_socket.send(res_bytes)
    new_socket.send(data)

    # 7. close the socket todo 貌似一次发送的内容太少时, 底层的缓冲区没满, 不会发送消息
    new_socket.close()  # 关闭socket会强制刷新底层的缓冲区, 即再发送一次消息



