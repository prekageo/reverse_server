#!/usr/bin/env python

"""Implement the remote endpoint of the reverse server."""

import logging

import reverse_server_common as common

# The following address is the remote server you'd like to connect to
REMOTE_SERVER_ADDRESS = ('ssh.server.in.my.firewalled.lan',22)

# The following address is where the reverse_server_local is running
DISPATCHER_ADDRESS = ('myhomepc.ath.cx',common.DISPATCHER_PORT)

def connect_to_dispatcher(address):
    """Connect to the dispatcher."""
    return common.log_and_connect(address, 'dispatcher')

def wait_for_dispatcher(socket):
    """
    Wait for a signal from the dispatcher in order to connect to the remote
    server.
    """
    excess_data = common.expect(socket, common.LOCAL_TO_REMOTE_MESSAGE)
    return excess_data

def connect_to_remote_server(address):
    """Connect to the remote server."""
    return common.log_and_connect(address, 'remote server')

def answer_to_dispatcher(socket):
    """
    Send a message to the dispatcher to inform that the connection with the
    remote server is ready.
    """
    logging.debug('Sending %s to initiator %s.' % (common.REMOTE_TO_LOCAL_MESSAGE,socket.getpeername()))
    socket.sendall(common.REMOTE_TO_LOCAL_MESSAGE)

def relay(socket1, socket2, excess_data_from_socket1):
    """Relay data between the dispatcher and the remote server."""
    common.relay(socket1,socket2,excess_data_from_socket1,None)

def main():
    """Main program."""
    logging.basicConfig(level=logging.INFO)
    logging.info('Reverse server remote started.')

    disp_socket = connect_to_dispatcher(DISPATCHER_ADDRESS)
    excess_data = wait_for_dispatcher(disp_socket)
    remote_socket = connect_to_remote_server(REMOTE_SERVER_ADDRESS)
    answer_to_dispatcher(disp_socket)
    relay(disp_socket, remote_socket, excess_data)

if __name__ == '__main__':
    main()
