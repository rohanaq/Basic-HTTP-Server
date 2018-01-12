import socket
import select
import sys
import os
from ConfigParser import SafeConfigParser
import subprocess

parser = SafeConfigParser()
parser.read('httpserver.conf')
for name in parser.options('http_port'):
    string_port = parser.get('http_port', name)
    value_port = parser.getint('http_port', name)
    # print value_port

server_address = ('localhost', value_port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)                       
            
            else:                
                data = sock.recv(4096)                                                                
                print data                                  
                
                request_header = data.split('\r\n')
                request_file = request_header[0].split()[1]
                
                get_php = None
                get_html = None
                if ".php" in request_file:
                    strip_php = request_file.strip('php')
                    get_php = strip_php + str('php')
                    get_path = os.getcwd() + get_php
                elif ".html" in request_file:
                    strip_html = request_file.strip('html')
                    get_html = strip_html + str('html')
                    get_path = os.getcwd() + get_html
                else:
                    get_path = os.getcwd() + request_file
                
                print "Get PHP: " + str(get_php)
                print "Get Path: " + get_path 
                print "Get HTML: " + str(get_html)
                print "is file: " + str(os.path.isfile(request_file)) + "\n"

                if request_file == 'index.html' or request_file == '/':                
                    f = open('index.html', 'r')
                    response_data = f.read()
                    f.close()
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'                    
                    sock.sendall(response_header + response_data)
                elif request_file == '' or request_file == '/dataset/':
                    path = "./dataset"
                    dirList = os.listdir(path)
                    konten = []
                    for files in dirList:
                       konten.append('<a href="'+format(files)+'">'+format(files)+'</a>')
                    response_data = "<br>".join(konten)
                    print response_data
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'    
                    sock.sendall(response_header + response_data)
                
                elif request_file == get_php:
                        proc = subprocess.Popen("php " + get_path, shell=True, stdout=subprocess.PIPE)
                        script_response = proc.stdout.read()
                        content_length = len(script_response)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'                    
                        sock.sendall(response_header + script_response)
                elif request_file == get_html:
                    f = open(get_path, 'r')
                    response_data = f.read()
                    f.close()
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'                    
                    sock.sendall(response_header + response_data)
                elif os.path.isfile("."+request_file):
                        f = open('.'+request_file, 'rb')
                        response_data = f.read()
                        f.close()
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/multipart; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n' 
                        sock.sendall(response_header + response_data)
                
                elif request_file and request_file != get_php :
                    if os.path.isfile("."+request_file):
                        f = open('.'+request_file, 'rb')
                        response_data = f.read()
                        f.close()
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/multipart; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n' 
                        sock.sendall(response_header + response_data)
                        
                    if request_file == '/dataset' or request_file == '/dataset/':
                        path = "./dataset"
                        dirList = os.listdir(path)
                        konten = []
                        for files in dirList:
                           konten.append('<a href="/dataset/'+format(files)+'">'+format(files)+'</a>')
                        response_data = "<br>".join(konten)
                        print response_data
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'    
                        sock.sendall(response_header + response_data)

                    else:
                        f = open('404.html', 'r')
                        response_data = f.read()
                        f.close()
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'    
                        sock.sendall(response_header + response_data)

                else:
                    f = open('404.html', 'r')
                    response_data = f.read()
                    f.close()
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' + str(content_length) + '\r\n\r\n'    
                    sock.sendall(response_header + response_data)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)   