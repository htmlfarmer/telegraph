import SocketServer
import datetime

# https://docs.python.org/2/library/socketserver.html
class MyTCPHandler(SocketServer.BaseRequestHandler):

    # Override "handle(self)" Method Used in SocketServer
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper() + str(datetime.datetime.now()))

    def GET_REQUEST(this):
     if this.path.find('?') != -1:
         this.path, this.query_string = \
             this.path.split('?', 1)
     else:
         this.query_string = ''
         this.send_response(200)
         this.send_header('Content-type', 'text/html')
         this.end_headers()
         this.globals = \
         dict(cgi.parse_qsl(this.query_string))
         sys.stdout = this.wfile
         this.wfile.write("<H2>Handle Get</H2><P>")
         this.wfile.write( \
            "<LI>Executing <B>%s</B>" % (this.path))
         this.wfile.write( \
             "<LI>With Globals<B>%s</B><HR>" % \
             (this.globals))
    #execfile(this.path, this.globals)
    #os.chdir('/myTest')

if __name__ == "__main__":
    HOST, PORT = "localhost", 9996
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
