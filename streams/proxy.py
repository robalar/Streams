"""
Author: robalar <rbthales@gmail.com>
URL: github.com/robalar/Streams

This file is part of streams

Streams is free software, and is distributed under the MIT licence.
See LICENCE or opensource.org/licenses/MIT
"""
from lib import socks
import socket
orginal_socket = socket.socket

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
socket.getaddrinfo = getaddrinfo


import stem
import stem.control
import logging
import json
import requesocks
import os
import platform
import subprocess

import streams

logger = logging.getLogger(__name__)

class TorProxy(object):

    TOR_PATH = streams.FULL_PATH + '\\tor\\Tor'
    
    def __init__(self):
        """Start the tor proxy & get ip info"""

        #Add config file varibles
        self.__dict__.update(streams.read_cfg('tor.cfg'))

        proxy =  ''.join([self.PROXY_URL, ':', str(self.SOCKS_PORT)])
        self.PROXIES = {'http': proxy, 'https': proxy}
        
        #is tor in the path?
        try:
            subprocess.call('tor --version')
        except OSError:
            if streams.PLATFORM == 'Windows':
                os.environ["PATH"] += os.pathsep + self.TOR_PATH
                print os.environ["PATH"]
            if streams.PLATFORM.startswith('Linux'):
                logger.error('Please install tor with your distributions\
                              package mangager or from source')
            
        #start tor
        logger.info('Starting tor')
        logger.info('proxy: {0}'.format(self.PROXIES['http']))

        tor_cfg = {'SocksPort':str(self.SOCKS_PORT),
                   'ExcludeNodes': self.EXCLUDE_EXIT_NODES,
                   'ControlPort':str(self.CONTROL_PORT)}
        
        try:
            self.proc = stem.process.launch_tor_with_config(config=tor_cfg,
                                                            take_ownership=True)
        except Exception as exc:
            logger.error('Error starting tor, are you running two instances?')
            raise exc

        #getting tor controller
        self.controller = stem.control.Controller.from_port(port=
                                                            self.CONTROL_PORT)
        self.controller.authenticate()

        streams.PROXIES = self.PROXIES

        log_ip_info()    
    
    def new_identity(self):
        #Only gets new identity if tor will accept
        if self.controller.is_newnym_available():
            logger.info('Getting new tor identity')
            self.controller.signal(stem.Signal.NEWNYM)
            log_ip_info()
        else:
            logger.warning(
                'Cannot get new tor identity. Wait {0} seconds'.format(
                    self.controller.get_newnym_wait()))  
    def kill(self):
        logger.info('Killing tor proxy')
        self.controller.close()
        self.proc.kill()

   
def log_ip_info():
    #get ip and location info
    print streams.PROXIES
    ip_info = json.loads(requesocks.get('http://ip-api.com/json',
                                        proxies=streams.PROXIES).text)
    logger.info('IP address: {0}'.format(ip_info['query']))
    logger.info('Location: {0}'.format(ip_info['country']))

        
