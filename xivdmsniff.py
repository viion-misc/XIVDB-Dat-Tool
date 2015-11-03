# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import socket
import struct
from os import path, makedirs
from configparser import SafeConfigParser

from xivdm.logging_utils import set_logging

def run(args, conf):
    output_path = path.join(conf.get('output', 'path'), 'all')

    # the public network interface
    HOST = socket.gethostbyname(socket.gethostname())

    # create a raw socket and bind it to the public interface
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((HOST, 0))

    # Include IP headers
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packages
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # receive a packet
    while True:
        packet = s.recvfrom(65565)
         
        #packet string from tuple
        packet = packet[0]
         
        #take first 20 characters for the ip header
        ip_header = packet[0:20]
         
        #now unpack them :)
        iph = struct.unpack('!BBHHHBBH4s4s' , ip_header)
         
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
         
        iph_length = ihl * 4
         
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])
         
        print('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr))
         
        tcp_header = packet[iph_length:iph_length+20]
         
        #now unpack them :)
        tcph = struct.unpack('!HHLLBBHHH' , tcp_header)
         
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
         
        print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))
         
        h_size = iph_length + tcph_length * 4
        data_size = len(packet) - h_size
         
        #get data from the packet
        data = packet[h_size:]
         
        print('Data : ' + str(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xivdm packet sniffer')
    subparsers = parser.add_subparsers(title='sub modules')

    ######################
    # Run sub module     #
    ######################
    run_parser = subparsers.add_parser('run', help='run sniffer')
    run_parser.set_defaults(callback=run)

    args = parser.parse_args()

    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmsniff')

    logging.info('Executing command: ' + str(sys.argv))

    if not hasattr(args, 'callback'):
        logging.error('Command-line parsing error.')
        parser.print_help()
    else:
        args.callback(args, config)
