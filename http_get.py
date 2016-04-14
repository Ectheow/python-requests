import os
import socket
import re

class HTTPResponeException(Exception):
    pass
class HTTPResponse:
    def __init__(self, string):
        self.http_version = None
        self.return_code = None
        self.code_explanation = None
        self.content_type = None
        self.content = ''
        self.content_length = 0
        self.headers = {}
        self.ok = False
        self._parse(string)
    def _parse(self, string):
        lines = string.split('\r\n')

        match =  re.match(
                'HTTP/(\d\.\d)\s(\d\d\d)\s([\w\s]*)',
                lines[0])
        if match:
            self.http_version = match.group(1)
            self.return_code = match.group(2)
            if (self.return_code[0] == '2'):
                self.ok = True
            self.code_explanation = match.group(3)
        else:
            raise HTTPResponseException("Bad HTTP response, no status line")

        lines.pop(0)

        while len(lines) > 0:
            line = lines[0]
            if line == '':
                break
            field_name, field_value = line.split(":")

            field_name = field_name.lower().strip()
            field_value = field_value.lower().strip()
            self.headers[field_name] = field_value
            if field_name == 'content-type':
                self.content_type = field_value
            lines.pop(0)

        lines.pop(0)
        self.content = os.linesep.join(lines)

class HTTPRequest:
    BUFSIZ = 1024
    def __init__(self):
        pass
    def parse_url(self, url):
        regex = '^(\w+)://([\w\d\.]+):?(\d*)([\w\d\/\?\%\.]*)$'
        match = re.match(regex, url)
        if (match.group(3) == ''):
            portno = socket.getservbyname(match.group(1))
        else:
            portno = int(match.group(3))
        return (
                match.group(1),
                match.group(2),
                portno,
                match.group(4))

    def get(self, url):
        proto, domain_name, port, obj = self.parse_url(url)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = socket.gethostbyname(domain_name)
            sock.connect((ip, port))
            request = 'GET %s HTTP/1.1\r\n\r\n' % obj
            sock.send(request)
            return sock.recv(HTTPRequest.BUFSIZ)
        except:
            raise
