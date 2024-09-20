codeDict = {
    "200": "OK",
    "404": "Not Found"
}


class HttpRequest:

    def __init__(self, request=None):
        if not request:
            self.method = "GET"
            self.url = "/"
            self.protocol = "HTTP/1.1"
            self.headers = {}
            self.body = b""
            return

        packet_split = request.split(b"\r\n\r\n")

        # 1. handle the method, url, proto, headers in packet_spit[0]
        head_part = packet_split[0].decode("UTF-8")
        headList = head_part.split("\r\n")

        # method, url, proto in headList[0]
        self.method, self.url, self.protocol = headList[0].split(" ")
        # headers
        self.headers = {}
        for i in range(1, len(headList)):
            k, v = headList[i].split(":", 1)
            self.headers[k] = v.strip()

        # 2. handle the request body
        self.body = packet_split[1]

    def getHeader(self, header):
        return self.headers.get(header)

    def setHeader(self, header, value):
        self.headers[header] = value

    def encode(self):
        req = f"{self.method} {self.url} {self.protocol}\r\n"
        for h, v in self.headers.items():
            req += f"{h}: {v}\r\n"
        req += "\r\n"
        req_bytes = req.encode("UTF-8")
        req_bytes += self.body
        return req_bytes

    def __str__(self):
        req = f"{self.method} {self.url} {self.protocol}\r\n"
        for h, v in self.headers.items():
            req += f"{h}: {v}\r\n"
        req += "\r\n"

        # format the body according to the content-type
        content_type = self.getHeader("Content-Type")
        if content_type and content_type.split("/")[0] == "text":
            req += self.body.decode("UTF-8")
        else:
            req += f"({len(self.body)} bytes in body)"
        return req


class HttpResponse:

    def __init__(self, response=None):
        if not response:
            self.protocol = "HTTP/1.1"
            self.code = 200
            self.msg = codeDict.get(str(200))
            self.headers = {}
            self.body = b""
            return

        packet_split = response.split(b"\r\n\r\n")

        # 1. handle the proto, code, msg, headers in packet_spit[0]
        head_part = packet_split[0].decode("UTF-8")
        headList = head_part.split("\r\n")

        # method, url, proto in headList[0]
        self.protocol, self.code, self.msg = headList[0].split(" ")
        # headers
        self.headers = {}
        for i in range(1, len(headList)):
            k, v = headList[i].split(":", 1)
            self.headers[k] = v.strip()

        # 2. handle the request body
        self.body = packet_split[1]

    def getHeader(self, header):
        return self.headers.get(header)

    def setHeader(self, header, value):
        self.headers[header] = value

    def encode(self):
        response = f"{self.protocol} {self.code} {self.msg}\r\n"
        for h, v in self.headers.items():
            response += f"{h}: {v}\r\n"
        response += "\r\n"
        res_bytes = response.encode("UTF-8")
        res_bytes += self.body
        return res_bytes

    def __str__(self):
        res = f"{self.protocol} {self.code} {self.msg}\r\n"
        for h, v in self.headers.items():
            res += f"{h}: {v}\r\n"
        res += "\r\n"
        # format the body according to the content-type
        content_type = self.getHeader("Content-Type")
        if content_type and content_type.split("/")[0] == "text":
            length = self.getHeader("Content-Length")
            if length and int(length) > 50:
                res += self.body[0:50].decode("UTF-8")
                res += "...\r\n"
                res += f"({int(length) - 50} bytes left...)"
            else:
                res += self.body.decode("UTF-8")
        else:
            res += f"({len(self.body)} bytes in body)"

        return res




def encodeBody():
    pass


def decodeBody():
    pass
