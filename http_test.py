import unittest
from http_get import *

class HTTPTestBasic(unittest.TestCase):
    def test_url_parse(self):
        http = HTTPRequest()
        self.assertEqual(
                ("http", "google.com", 80, "/index.html"),
                http.parse_url("http://google.com/index.html"))
        self.assertEqual(
                ("http", "reddit.com", 80, "/doodle/cat/moodle"),
                http.parse_url("http://reddit.com/doodle/cat/moodle"))
    def test_get(self):
        http = HTTPRequest()
        print(http.get('http://www.google.com/'))

class HTTPParserTestBasic(unittest.TestCase):
    def test_http_parse(self):
        content = bytearray('hello, world')
        string = bytearray(
b"HTTP/1.1 200 OK\r\n\
Connection: Close\r\n\
Server: Garble\r\n\
Content-Type: text/html\r\n\
Content-Length: %d\r\n\
\r\n\
%s" % (len(content), content))
        resp = HTTPResponse(string)
        self.assertEqual(resp.return_code, '200')
        self.assertEqual(resp.http_version, '1.1')
        self.assertTrue(resp.ok)
        self.assertEqual(resp.headers,
            {'connection':'close',
             'content-type':'text/html',
             'content-length':str(len(content)),
             'server': 'garble'})
        self.assertEqual(resp.content, content)
        

if __name__ == '__main__':
    unittest.main()
