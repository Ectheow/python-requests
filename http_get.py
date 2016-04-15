import os
import logging
import socket
import re

class HTTPResponseException(Exception):
    pass
class HTTPResponse:
    HTTP_LINESEP=bytearray('\r\n')
    def __init__(self, string):
        self.http_version = None
        self.return_code = None
        self.code_explanation = None
        self.content = ''
        self.content_length = None
        self.headers = {}
        self.ok = False
        self._parse(string)
    
    def __get_next_line(self, bytestr):
        line = None

        while(len(bytestr) > 0):
            if line is None:
                line = bytearray()
            if bytestr[0:2] ==  HTTPResponse.HTTP_LINESEP:
                bytestr.pop(0)
                bytestr.pop(0)
                break
            else:
                line.append(bytestr.pop(0))
        return line

    def _header_status(self, bytestr):
        '''
        Parse the status line of the request response.
        Should be like:

        HTTP/1.1 200 OK

        Or something of the kind.

        To quote rfc7230:

            The first line of a response message is the status-line
            consisting of the protocol version, a space (SP), the
            status code, another space, a possibly empty textual
            phrase describing the status code, and ending with a CRLF. 

            status-line = HTTP-version SP status-code SP reason-phrase
            CRLF
        '''

        line = self.__get_next_line(bytestr)
        if not line:
            raise HTTPResponseException("Bad HTTP response")

        line = line.decode('ASCII')
        match =  re.match(
            '^HTTP/(\d\.\d)\s(\d\d\d)\s([\w\s]*)$',
            line)
        if match:
            self.http_version = match.group(1)
            self.return_code = match.group(2)
            if (self.return_code[0] == '2'):
                self.ok = True
            self.code_explanation = match.group(3)
        else:
            raise HTTPResponseException(
                    "Bad HTTP response, no status line or invalid status line")

    def _header_fields(self, bytestr):
        bytesline = self.__get_next_line(bytestr)
        while(bytesline is not None and len(bytesline) != 0):
            line = bytesline.decode('ASCII')
            if not line.find(":"):
                raise HTTPResponseException(
                "Bad HTTP header field: %s", line)
            field_name, field_value = line.split(":")
            field_name = field_name.lower().strip()
            field_value = field_value.lower().strip()
            self.headers[str(field_name)] = str(field_value)

            if field_name == 'content-length':
                self.content_length = int(field_value)
            bytesline = self.__get_next_line(bytestr)

    def _content(self, bytestr):
        self.content = bytestr
        if self.content_length is not None:
            if len(bytestr) != self.content_length:
                raise HTTPResponseException(
                "HTTP content not correct length")

    def _parse(self, string):
        assert type(string) == bytearray
        self._header_status(string)
        self._header_fields(string)
        self._content(string)

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
