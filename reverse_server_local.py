#!/usr/bin/env python

"""Implement the local endpoint of the reverse server."""

import logging
import socket
import threading

import reverse_server_common as common

LOCAL_SERVER_PORT_START = 5000

class Connection(threading.Thread):
    """Handle a connection received from an initiator."""
    local_server_port = LOCAL_SERVER_PORT_START

    def __init__(self, initiator_socket):
        """Initialize a connection."""
        super(Connection, self).__init__()
        self.initiator_socket = initiator_socket
        self.initiator_address = self.initiator_socket.getpeername()

    def run(self):
        """Main thread loop."""
        logging.debug('Got connection from initiator %s.' % str(self.initiator_address))
        local_server_socket = self.open_local_server()
        self.announce()
        local_socket = self.wait_local_client_connection(local_server_socket)
        self.send_to_initiator()
        excess_data = self.wait_initiator()
        self.relay(self.initiator_socket,local_socket,excess_data)

    def open_local_server(self):
        """Open local server."""
        self.local_server_port = Connection.local_server_port
        Connection.local_server_port += 1

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.local_server_port))
        sock.listen(1)
        return sock

    def announce(self):
        """
        Announce the connection from an initiator and the local port to use.
        """
        logging.info('Start local server (port %d for %s).' % (self.local_server_port,self.initiator_address))

    def wait_local_client_connection(self, socket):
        """Wait for a local client to connect on the local server."""
        local_socket, tcp_addr = socket.accept()
        logging.debug('Got connection to local server from %s.' % str(tcp_addr))
        return local_socket

    def send_to_initiator(self):
        """Send a message to the initiator to begin the remote connection."""
        logging.debug('Sending %s to initiator %s.' % (common.LOCAL_TO_REMOTE_MESSAGE,self.initiator_address))
        self.initiator_socket.sendall(common.LOCAL_TO_REMOTE_MESSAGE)

    def wait_initiator(self):
        """Wait the initiator to signal that the remote connection is ready."""
        excess_data = common.expect(self.initiator_socket, common.REMOTE_TO_LOCAL_MESSAGE)
        return excess_data

    def relay(self, socket1, socket2, excess_data_from_socket1):
        """Relay data between the local client and the initiator."""
        common.relay(socket1, socket2, excess_data_from_socket1,None)

def open_dispatcher():
    """Open the dispatcher and start listening."""
    logging.debug('Start dispatcher (port %d).',common.DISPATCHER_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', common.DISPATCHER_PORT))
    sock.listen(1)
    return sock

def accept_initiator(socket):
    """Accept a connection from an initiator."""
    initiator_socket, _ = socket.accept()
    conn = Connection(initiator_socket)
    conn.start()

def main():
    """Main program."""
    logging.basicConfig(level=logging.INFO)
    logging.info('Reverse server local started.')

    disp_socket = open_dispatcher()
    while 1:
        accept_initiator(disp_socket)

if __name__ == '__main__':
    main()
