"""Provide common functions for the reverse server."""

import logging
import select
import socket

DISPATCHER_PORT = 80
LOCAL_TO_REMOTE_MESSAGE = 'GO!'
REMOTE_TO_LOCAL_MESSAGE = 'OK.'

def log_and_connect(address, description):
    """Create a TCP connection to address and log the attempt."""
    logging.debug('Trying to connect to %s at %s.' % (description,address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(address)
    except Exception, e:
        logging.error('Connection failed: %s.' % e)
        return None
    logging.debug('Connected to %s at %s.' % (description,address))
    return sock

def expect(socket, data):
    """
    Wait on the socket for data to arrive and return the excess data received.
    """
    logging.debug('Expecting %s from %s.' % (data,socket.getpeername()))

    big_buffer = ''

    while len(big_buffer)<len(data):
        buffer = socket.recv(4096)
        if not buffer:
            break
        big_buffer += buffer

    if big_buffer[:len(data)] == data:
        logging.debug('Got %s from %s.' % (data,socket.getpeername()))
        excess = big_buffer[len(data):]
    else:
        logging.error('Socket %s sent garbage: [%s].' % (socket.getpeername(),big_buffer))
        excess = big_buffer

    return excess

def relay(socket1, socket2, data1=None, data2=None):
    """
    Relay data between socket1 and socket2. data1 and data2 are initial data to
    be sent between the sockets.
    """
    def log_and_send(source, dest, data):
        if data != None:
            logging.debug('Relay %s->%s: [%s].' % (source.getpeername(), dest.getpeername(), data))
            dest.sendall(data)

    log_and_send(socket1, socket2, data1)
    log_and_send(socket2, socket1, data2)

    abort = False
    while not abort:
        ready_list,_,_ = select.select([socket1, socket2],[],[])
        for ready in ready_list:
            buffer = ready.recv(4096)

            if not buffer:
                abort = True
                break

            if ready == socket1:
                target = socket2
            else:
                target = socket1

            log_and_send(ready, target, buffer)

    logging.debug('Closing connection with %s.' % (socket1.getpeername(),))
    socket1.close()
    logging.debug('Closing connection with %s.' % (socket2.getpeername(),))
    socket2.close()
