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
        string = (
"HTTP/1.1 200 OK\r\n\
Connection: Close\r\n\
Server: Garble\r\n\
Content-Type: text/html\r\n\
\r\n\
<html></html>\r\n")
        resp = HTTPResponse(string) 
        self.assertEqual(resp.content, '<html></html>\n')
        self.assertEqual(resp.return_code, '200')
        self.assertEqual(resp.http_version, '1.1')
        self.assertTrue(resp.ok)
        self.assertEqual(resp.headers,
            {'connection':'close',
             'content-type':'text/html',
             'server': 'garble'})


if __name__ == '__main__':
    unittest.main()
