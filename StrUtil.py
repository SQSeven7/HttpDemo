import re
import os

import Http

MIME_dict = {
    ".txt": "text/plain",
    ".html": "text/html",
    ".css": "text/css",
    ".js": "text/javascript",
    ".png": "image/png",
    ".jpp": "image/jpeg",
}

packet = "POST / HTTP/1.1\r\n" \
         "Host: localhost\r\n" \
         "Connection: keep-alive\r\n" \
         "Content-Length: 377\r\n" \
         "Cache-Control: max-age=0\r\n" \
         "Origin: http://localhost\r\n" \
         "Content-Type: multipart/form-data; boundary=----WebKitFormBoundarypa1MgWfzF9twAx2f\r\n" \
         "\r\n" \
         "------WebKitFormBoundarypa1MgWfzF9twAx2f\r\n" \
         "Content-Disposition: form-data; name=\"myFile\"; filename=\"text.txt\"\r\n" \
         "Content-Type: text/plain\r\n" \
         "\r\n" \
         "**text**\r\n" \
         "------WebKitFormBoundarypa1MgWfzF9twAx2f\r\n" \
         "Content-Disposition: form-data; name=\"name\"\r\n" \
         "\r\n" \
         "OY\r\n" \
         "------WebKitFormBoundarypa1MgWfzF9twAx2f--\r\n"


def matchPath(request):
    ma = re.search(r"(/.*) ", request)
    return ma.group(1)


def getMIME(ext):
    return MIME_dict.get(ext)


def httpPacket(status, mime, length):
    desc = "OK" if status == 200 else "Not Found"
    return f"HTTP/1.1 {status} {desc}" \
           f"\r\n" \
           f"Content-Type: {mime}" \
           f"\r\n" \
           f"Content-Length: {length}" \
           f"\r\n" \
           f"Connection: close" \
           f"\r\n" \
           f"\r\n"


if __name__ == '__main__':


    pass
    # print([item.split(";") for item in request.getHeader("Content-Type").split(",")])
    # print("/img.p/ng".split("/", 1))
    # with open("img.png", "rb") as fp:
    #     data = fp.read()
    #     print(len(data))
    # path = matchPath("GET /img.png HTTP/1.1\r\nHost: localhost")
    # print(path)
    # split = os.path.split(path)
    # print(os.path.splitext(split[1])[1])
