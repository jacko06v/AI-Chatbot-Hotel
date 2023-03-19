from http.server import BaseHTTPRequestHandler, HTTPServer
#import process_response function from chatbot.py
from chatbot import process_response, trainModel

class RequestHandler_httpd(BaseHTTPRequestHandler):
    
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes('''
            Server Hotel Devon chatbot: Service up and running.<br/><br/> Please, use the right protocol to communicate at this address. <br/><br/>To know more, feel free to contact us at the address: jacomosconi@gmail.com or on jacopomosconi.com.<br/><br/> Cu Mate!<br/><br/><pre style="line-height: 0.7;">
               ,'``.._   ,'``. <br/>
              :,--._:)\,:,._,.:       All Glory to <br/>
              :`--,''   :`...';\      the HYPNO TOAD! <br/>
               `,'       `---'  `. <br/>
               /                 :<br/> 
              /                   \<br/>
            ,'                     :\.___,-.<br/>
           `...,---'``````-..._    |:       \<br/>
             (                 )   ;:    )   \  _,-.<br/>
              `.              (   //          `'    \<br/>
               :               `.//  )      )     , ;<br/>
             ,-|`.            _,'/       )    ) ,' ,'<br/>
            (  :`.`-..____..=:.-':     .     _,' ,'<br/>
             `,'\ ``--....-)='    `._,  \  ,') _ '``._<br/>
          _.-/ _ `.       (_)      /     )' ; / \ \`-.'<br/>
         `--(   `-:`.     `' ___..'  _,-'   |/   `.)<br/>
             `-. `.`.``-----``--,  .'<br/>
               |/`.\`'        ,','); <br/>
                   `         (/  (/<br/>
</pre>
'''
, "utf-8"))
            
        def do_POST(self):
            message = self.path.split('?message=')[1]
            message = message.replace('-', ' ')

            self.path = self.path.split('?')[0]


            if self.path == '/chat':
                response = process_response(message)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write('Not found'.encode('utf-8'))
          
def run():
    print('training model...')
    trainModel()
    print('model trained')
    print('starting server...')
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, RequestHandler_httpd)
    print('running server...')
    httpd.serve_forever()

run()
