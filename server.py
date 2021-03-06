import sys
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from pymongo import MongoClient


Protocol = "HTTP/1.1"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 9000

server_address = ("", port)


class myHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content_type", "text/html")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        if parsed.path == "/query":
            field = urlparse.parse_qs(parsed.query)['field'][0]
            mongo_client = MongoClient()
            db = mongo_client['test']
            if field + '_single_word' not in db.collection_names():
                self.send_response(404)
            else:
                single = db[field + '_single_word']
                top_words = single.find().limit(20)
                message = []

                for word in top_words:
                    a_word = {'word': word['word']}
                    if len(word['cluster']) > 0:
                        a_word['cluster'] = word['cluster']
                    message.append(a_word)

                double = db[field + '_phrase']
                top_phrases = double.find().limit(10)
                for phrase in top_phrases:
                    a_phrase = {'word': phrase['word']}
                    message.append(a_phrase)

                self.send_response(200)
                self.send_header("Content_type", "text/html")
                self.end_headers()

                self.wfile.write('<!DOCTYPE html>')
                self.wfile.write('<html">')
                self.wfile.write('<head lang="en">')
                self.wfile.write('<meta charset="UTF-8">')
                self.wfile.write('<title>%s hot topics</title>' % field.upper())
                self.wfile.write('</head>')
                self.wfile.write('<body>')
                self.wfile.write('<div>')
                self.wfile.write('<h1 style="color: brown;">TrendyWriter</h1>')
                self.wfile.write('<h2 style="color: brown;">You will never miss a trend..</h2>')
                self.wfile.write('<hr>')
                self.wfile.write('<h1 style="color: blue;">- Selected Field:</h1>')
                self.wfile.write('<h2>%s</h2>' % field)
                self.wfile.write('<h1 style="color: blue;">- Here is the Trending Topics Right Now:</h1>')
                for item in message:
                    self.wfile.write('<li><h2>%s</h2></li>' % item['word'])
                self.wfile.write('</div>')
                self.wfile.write('</body>')
                self.wfile.write('</html>')
        elif parsed.path == "/cluster":
            field = urlparse.parse_qs(parsed.query)['field'][0]
            name = urlparse.parse_qs(parsed.query)['cname'][0]
            mongo_client = MongoClient()
            db = mongo_client['test']
            if field + '_clusters' not in db.collection_names():
                self.send_response(404)
            else:
                clus = db[field + '_clusters']
                cluster_wanted = clus.find({"name": name}).limit(1)
                message = cluster_wanted[0]['words']
                self.send_response(200)
                self.send_header("Content_type", "text/html")
                self.end_headers()
                self.wfile.write('<!DOCTYPE html>')
                self.wfile.write('<html">')
                self.wfile.write('<head lang="en">')
                self.wfile.write('<meta charset="UTF-8">')
                self.wfile.write('<title>%s relative words</title>' % field.upper())
                self.wfile.write('</head>')
                self.wfile.write('<body>')
                self.wfile.write('<div>')
                self.wfile.write('<h1 style="color: brown;">TrendyWriter</h1>')
                self.wfile.write('<h2 style="color: brown;">You will never miss a trend..</h2>')
                self.wfile.write('<hr>')
                self.wfile.write('<h1 style="color: blue;">- Selected Field:</h1>')
                self.wfile.write('<h2>%s</h2>' % field.upper())
                self.wfile.write('<h1 style="color: blue;">- Selected Cluster:</h1>')
                self.wfile.write('<h2>%s</h2>' % name)
                self.wfile.write('<h1 style="color: blue;">- Here is All Relative Topics in the Cluster:</h1>')
                for item in message:
                    self.wfile.write('<li><h2>%s</h2></li>' % item)
                self.wfile.write('</div>')
                self.wfile.write('</body>')
                self.wfile.write('</html>')

if __name__ == '__main__':
    httpd = HTTPServer(server_address, myHandler)

    sa = httpd.socket.getsockname()
    print "HTTP Server running on", sa[0], "port", sa[1], "..."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

