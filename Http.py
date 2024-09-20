statusDict = {
    "200": "OK",
    "404": "Not Found"
}


class HttpRequest:

    def __init__(self, request):
        packet_split = request.split("\r\n\r\n")

        # 1. handle the method, url, proto, headers in packet_spit[0]
        headList = packet_split[0].split("\r\n")

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

    def __init__(self, status):
        self.protocol = "HTTP/1.1"
        self.status = status
        self.desc = statusDict.get(status + "")
        self.headers = {}
        self.body = b""

    def getHeader(self, header):
        return self.headers.get(header)

    def __str__(self):
        response = f"{self.protocol} {self.status} {self.desc}\r\n"
        for h, v in self.headers.items():
            response.join(f"{h}: {v}\r\n")
        response.join("\r\n")
        response.join(self.body)

        return response




def encodeBody():
    pass


def decodeBody():
    pass
