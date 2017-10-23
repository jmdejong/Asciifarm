
HEADER_SIZE = 4


# this module is for sending discree messages over TCP
# this is achieved by prefixing all messages with their length
# calls to send and recv will also keep attempting to send all data unless this proves impossible


def send(sock, msg):
    length = len(msg)
    header = length.to_bytes(4, byteorder="big")
    totalmsg = header + msg
    sock.sendall(totalmsg)

def receive(sock):
    header = recvall(sock, 4) #sock.recv(4)
    length = int.from_bytes(header, byteorder="big")
    return recvall(sock, length)

def recvall(sock, length):
    chunks = []
    bytes_recd = 0
    while bytes_recd < length:
        chunk = sock.recv(min(length - bytes_recd, 4096))
        if chunk == b'':
            break
            #raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)
    
