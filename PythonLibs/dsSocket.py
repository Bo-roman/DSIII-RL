import socket
from threading import Thread
import time

########## AUX FUNCTIONS ##########



#---------------------------------------------------------------

#returns a string
def recvMessage(connection):
    #first we need to get message length
    #we define a frame, where first we read the messagelength with
    #the termination of @ and then we read the remaining message
    iDataLength = 0
    sDataLength = ''
    while sDataLength[-1:] != '@':
        sDataLength = sDataLength + connection.recv(1).decode('utf-8')

    sDataLength = sDataLength[:-1]
    iDataLength = int(sDataLength)

    return connection.recv(iDataLength).decode('utf-8')

#returns dictionary {dataType : string, name : string , message : dataType }
def recvObject(connection):
    dataType = recvMessage(connection)
    name = recvMessage(connection)
    rawMessage = recvMessage(connection)
    
    message = ''

    if dataType == 'integer':
        message = int(rawMessage)
    elif dataType == 'float':
        message = float(rawMessage)
    elif dataType == 'string':
        message = rawMessage

    return {'dataType' : dataType,
            'name'     : name,
            'message'  : message
            }

#DSLR -> Dark souls reinforcment learning Object
#returns a simple one level deep json like object aka dictionary
def recvDSRLObject(connection):
    DSLRObject = {}
    currentObject = {}
    DSLRObjectLength = int(recvObject(connection)['message'])
    
    for i in range(DSLRObjectLength):
        currentObject = recvObject(connection)
        DSLRObject[currentObject['name']] = currentObject['message']
       
    return DSLRObject


def sendMessage(connection,message):
    connection.send((str(len(message)) + '@').encode())
    connection.send(message.encode())

def sendObject(connection,dataType,name,message):
    sendMessage(connection,dataType)
    sendMessage(connection,name)
    sendMessage(connection,message)

def sendDSRLObject(connection,Object):
    objectLength = len(Object)
    currentDataType = ''
    
    if objectLength == 0:
        return

    sendObject(connection,'integer','_length',str(objectLength))
    

    for key,value in Object.items():
        if type(value) == int:
            currentDataType = 'integer'
        elif type(value) == float:
            currentDataType = 'float'
        elif type(value) == str:
            currentDataType = 'string'

        sendObject(connection,currentDataType,key,str(value))


def createServer(port,callback):
    connectionThreads = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost',port))
    sock.listen()
    
    while True:
        print('Waiting for connection...')
        conn, addr = sock.accept()
        print('Connected by', addr)
        currentConnectionThread = Thread(target = callback, args = [conn])
        currentConnectionThread.start()
        connectionThreads.append(currentConnectionThread)

def connectToServer(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    return sock



    
    
