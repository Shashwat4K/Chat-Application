# SERVER CODE
# Update 1.1 AES Encryption Now Included :p
# AES Block Cipher 16 bytes block size as supported by pyaes
# You Can Change the Port Server Listens by passing argument in command line directly
# Server Code To be Started before Client, or Connection will be refused
# Author : xtreme.research@gmail.com

import os
try:
    import pyaes 
except ImportError:
    print("Install pyaes library!")
    print("windows : python -m pip insatll pyaes")
    print("linux   : pip install pyaes ")
    exit()
import sys
import socket
import threading
import hashlib

HOST = '0.0.0.0'
if(len(sys.argv)==1):
    PORT = 5558
elif(len(sys.argv)==2):
    PORT=int(sys.argv[1])

print("[+] Server Running ")
print("[+] Allowing All Incoming Connections ")
print("[+] PORT "+str(PORT))
print("[+] Waiting For Connection...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('[+] Connected by ', addr)

key = str(input("Enter AES Encryption Key For Connection : "))
hashed = hashlib.sha256(key.encode()).digest()
aes = pyaes.AES(hashed)

def process_bytes(bytess):
    ret = []
    while(len(bytess)>=16):
        if(len(bytess)>=16):
            byts = bytess[:16]
            ret.append(byts)
            bytess = bytess[16:]
        else:
            print("Block Size Mismatch ")
    return ret

def process_text(data): #take data in as a string return 16 bytes block of bytes list
    streams = []
    while (len(data)>0):
        if(len(data)>=16):
            stream = data[:16]
            data = data[16:]
        else:
            stream = data + ("~"*(16-len(data)))
            data = ''
        stream_bytes = [ ord(c) for c in stream]
        streams.append(stream_bytes)
    return streams

class myThread(threading.Thread):
    def __init__(self,id):
        threading.Thread.__init__(self)
        self.threadID = id

    def run(self):
        print("[+] Listening On Thread "+str(self.threadID))
        while 1:
            data = conn.recv(1024)
            if(data!=""):
                processed_data = process_bytes(data)
                print("Recieved : ",end="")
                for dat in processed_data:
                    decrypted = aes.decrypt(dat)
                    mess=''
                    for ch in decrypted:
                        if(chr(ch)!='~'):
                            mess+=str(chr(ch))
                    print (str(mess),end= "")
                print("")

Listening_Thread = myThread(1)
Listening_Thread.daemon = True
Listening_Thread.start()

while 1:
    sending_data = str(input(""))
    if(sending_data=="quit()"):

        exit()
    sending_bytes = process_text(sending_data)
    enc_bytes = []
    for byte in sending_bytes:
        ciphertext = aes.encrypt(byte)
        enc_bytes += bytes(ciphertext)
    #print("Sending : "+str(sending_data))
    conn.send(bytes(enc_bytes))
conn.close()
